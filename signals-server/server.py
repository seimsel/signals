from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType,
    MutationType
)

from ariadne.asgi import GraphQL

from starlette.applications import Starlette
from starlette.routing import Route, Mount
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

from signals.node import node_type
from signals.session import Session
from signals.measurement import Measurement
from signals.measurement_types.file_measurement import FileMeasurement
from signals.signal import Signal
development = os.environ.get('DEVELOPMENT', 'false') == 'true'

DPI = 96

style.use('./styles/dark.mplstyle')

query = QueryType()
mutation = MutationType()

@query.field('measurement')
async def resolve_session(obj, info, url):
    request = info.context['request']
    session = request.app.session(request)
    return session.measurement_with_url(url)

def figure(request):
    session = request.app.session(request)

    width = int(request.query_params['width'])
    height = int(request.query_params['height'])
    url = request.query_params['url']
    measurement = session.measurement_with_url(url)

    figure = Figure(
        figsize=(width/DPI, height/DPI),
        dpi=DPI
    )

    for signal in measurement.children:
        t = signal.t
        y = signal.y

        figure.gca().plot(t, y)
        buffer = BytesIO()
        figure.savefig(buffer, format='png', dpi=DPI)
        buffer.seek(0)
        image = buffer.read()
        buffer.close()

    return Response(image, media_type='image/png')

type_defs = load_schema_from_path('./schema')
schema = make_executable_schema(type_defs, query, mutation, node_type)

routes = [
    Route('/figure', endpoint=figure),
    Mount('/graphql', app=GraphQL(
        schema,
        debug=development
    ))
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

class Application(Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state.sessions = {}

    def session(self, request):
        session = request.session
        session_id = session.get('id', '')

        if not session_id or not session_id in self.state.sessions:
            session_object = Session()
            session['id'] = session_object.id
            self.state.sessions[session_object.id] = session_object
            return session_object
        
        return self.state.sessions[session_id]

app = Application(
    debug=True,
    routes=routes,
    middleware=middleware
)
