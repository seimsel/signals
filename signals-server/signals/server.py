from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType
)

from ariadne.asgi import GraphQL

from starlette.middleware.sessions import SessionMiddleware

from uuid import uuid4
import sys
import json

from .view import View
from .measurement import Measurement
from .channel import Channel

query = QueryType()

sessions = {}

@query.field('views')
def resolve_views(obj, info):
    session = info.context['request'].session

    if not 'id' in session:
        session['id'] = str(uuid4())

        view = View()
        measurement = Measurement()
        channel = Channel()
        subchannel = Channel()

        view.appendMeasurement(measurement)
        measurement.appendChannel(channel)
        channel.appendChannel(subchannel)

        sessions[session['id']] = {
            'views': [
                view
            ]
        }

    return sessions[session['id']]['views']

type_defs = load_schema_from_path('schema')
schema = make_executable_schema(type_defs, query)
app = SessionMiddleware(
    GraphQL(schema, debug=True),
    'Hello, World!'
)
