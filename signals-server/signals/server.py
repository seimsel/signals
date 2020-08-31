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

from .measurement import Measurement
from .channel import Channel

query = QueryType()

sessions = {}

@query.field('measurement')
def resolve_measurement(obj, info):
    session = info.context['request'].session

    if not 'id' in session:
        session['id'] = str(uuid4())

        measurement = Measurement('file://test.csv')
        channel = Channel()
        subchannel = Channel()

        measurement.appendChannel(channel)
        channel.appendChannel(subchannel)

        sessions[session['id']] = {
            'measurement': measurement
        }

    return sessions[session['id']]['measurement']

type_defs = load_schema_from_path('schema')
schema = make_executable_schema(type_defs, query)
app = CORSMiddleware(
    SessionMiddleware(
            GraphQL(schema, debug=True),
            secret_key='SECRET'
    ),
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
