from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType
)

from ariadne.asgi import GraphQL

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from uuid import uuid4
import sys
import json
import os

from .node import node_type
from .measurement import Measurement
from .channel import Channel

query = QueryType()

sessions = {}

@query.field('measurement')
def resolve_measurement(obj, info):
    session = info.context['request'].session

    if not 'id' in session:
        session['id'] = str(uuid4())

    if not session['id'] in sessions:
        sessions[session['id']] = {}

    if not 'measurement' in sessions[session['id']]:
        measurement = Measurement('file://test.csv')

        sessions[session['id']] = {
            'measurement': measurement
        }

    return sessions[session['id']]['measurement']

@query.field('node')
def resolve_node(obj, info, nodeId):
    session = info.context['request'].session

    measurement = sessions[session['id']]['measurement']

    return measurement.nodes[nodeId]

type_defs = load_schema_from_path('schema')
schema = make_executable_schema(type_defs, query, node_type)
app = SessionMiddleware(
    CORSMiddleware(
        GraphQL(schema, debug=True),
        allow_origins=[os.environ.get('UI_HTTP_URL')],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    ),
    secret_key='SECRET'
)
