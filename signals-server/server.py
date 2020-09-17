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

import uvicorn

# This is necessary so pyinstaller includes these modules
import uvicorn.logging
import uvicorn.loops
import uvicorn.loops.auto
import uvicorn.protocols
import uvicorn.protocols.http
import uvicorn.protocols.http.auto
import uvicorn.protocols.websockets
import uvicorn.protocols.websockets.auto
import uvicorn.lifespan
import uvicorn.lifespan.on

from uuid import uuid4
from pathlib import Path
from io import BytesIO
import os

from signals.node import node_type
from signals.session import Session
from signals.measurement import Measurement
from signals.measurement_types.file_measurement import FileMeasurement
from signals.signal import Signal
from signals.spa_staticfiles import SpaStaticFiles

development = os.environ.get('DEVELOPMENT', 'false') == 'true'

DPI = 96

style.use('./styles/dark.mplstyle')

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

@mutation.field('openFiles')
async def resolve_open_files(obj, info, urls, windowId):
    session = info.context['request'].session

    window = sessions[session['id']].window_with_id(windowId)
    
    for url in urls:
        window.add_measurement(FileMeasurement(url))

    return {
        'windows': [
            window
        ],
        'errors': []
    }

@mutation.field('closeMeasurement')
async def resolve_close_measurement(obj, info, measurementId, windowId):
    session = info.context['request'].session

    window = sessions[session['id']].window_with_id(windowId)
    
    window.remove_measurement(measurementId)

    return {
        'window': window,
        'error': None
    }

def figure(request):
    session = request.session
    width = int(request.query_params['width'])
    height = int(request.query_params['height'])
    measurementId = request.query_params['measurementId']
    measurement = sessions[session['id']].measurement_with_id(measurementId)

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
    )),
    Mount('/', app=SpaStaticFiles(
        directory='./static',
        html=True
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

app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware
)

if __name__ == '__main__':
    # This is necessary so pyinstaller includes the uvicorn.logging module
    uvicorn.run(
        'server:app' if development else app,
        reload=development,
        port=int(os.environ.get('SERVER_PORT', 8000))
    )
