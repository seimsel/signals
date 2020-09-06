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

from asyncio import sleep

from matplotlib.pyplot import style
from matplotlib.figure import Figure

from uuid import uuid4
from pathlib import Path
from io import BytesIO
from base64 import b64encode
import sys
import json
import os

from .node import node_type
from .measurement import Measurement
from .channel import Channel

DPI = 96

style.use(str(Path(__file__).with_name('dark.mplstyle')))

query = QueryType()
mutation = MutationType()

sessions = {}

@query.field('session')
async def resolve_session(obj, info):
    session = info.context['request'].session

    if not 'id' in session:
        session['id'] = str(uuid4())

    if not session['id'] in sessions:
        sessions[session['id']] = {}

    if not 'measurement' in sessions[session['id']]:
        measurement = Measurement('file://test.csv')
        channel = Channel(None, None)
        measurement.channels[0].appendChild(channel)
        measurement.channels[1].appendChild(channel)

        sessions[session['id']] = {
            'measurement': measurement
        }

    return session

@query.field('measurement')
async def resolve_measurement(obj, info):
    session = info.context['request'].session
    return sessions[session['id']]['measurement']

@query.field('nodes')
def resolve_nodes(obj, info):
    session = info.context['request'].session
    measurement = sessions[session['id']]['measurement']

    return measurement.nodes.values()

def figure(request):
    session = request.session
    measurement = sessions[session['id']]['measurement']

    width = int(request.query_params['width'])
    height = int(request.query_params['height'])

    figure = Figure(
        figsize=(width/DPI, height/DPI),
        dpi=DPI
    )

    for channel in measurement.channels:
        x = channel.x
        y = channel.y

        figure.gca().plot(x, y)
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
