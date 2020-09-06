from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType,
    MutationType
)

from ariadne.asgi import GraphQL

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from matplotlib.pyplot import style
from matplotlib.figure import Figure

from uuid import uuid4
from pathlib import Path
from io import BytesIO
import os

from .node import node_type
from .session import Session
from .measurement import Measurement
from .signal import Signal

DPI = 96

style.use(str(Path(__file__).with_name('dark.mplstyle')))

query = QueryType()
mutation = MutationType()

sessions = {}

@query.field('session')
async def resolve_session(obj, info):
    session = info.context['request'].session

    session_id = session.get('id', '')
    session_object = sessions.get(session_id, Session())

    if not session_id:
        session['id'] = session_object.id
    
    sessions[session_id] = session_object

    return session_object

def figure(request):
    session = request.session
    measurement = sessions[session['id']].windows[0].measurements[0]

    width = int(request.query_params['width'])
    height = int(request.query_params['height'])

    figure = Figure(
        figsize=(width/DPI, height/DPI),
        dpi=DPI
    )

    for signal in measurement.signals:
        t = signal.t
        y = signal.y

        figure.gca().plot(t, y)
        buffer = BytesIO()
        figure.savefig(buffer, format='png', dpi=DPI)
        buffer.seek(0)
        image = buffer.read()
        buffer.close()

    return Response(image, media_type='image/png')

type_defs = load_schema_from_path('schema')
schema = make_executable_schema(type_defs, query, mutation, node_type)

routes = [
    Route('/figure', endpoint=figure)
]

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key='SECRET'
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=[os.environ.get('UI_HTTP_URL')],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    )
]

app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware
)

app.mount('/graphql', 
    GraphQL(schema, debug=True),
)
