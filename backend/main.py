from io import BytesIO
from asyncio import sleep
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette as Application
from starlette.routing import Route
from starlette.responses import StreamingResponse
from ariadne import SubscriptionType
from vxi11 import Instrument
from drivers.lecroy_scope import LeCroyScope
from matplotlib.figure import Figure
from numpy.random import rand
from numpy import linspace

subscription = SubscriptionType()

@subscription.source('scope')
async def scope_generator(obj, info, address):
    scope = LeCroyScope(address)

    while True:
        wave_desc, wave_array_1 = scope.read()
        yield {
            'channels': [
                {
                    'waveform': {
                        'triggerTime': wave_desc.trigger_time
                    }
                }
            ]
        }
        await sleep(1)

@subscription.field('scope')
def scope_resolver(scope, info, address):
    return scope

async def figure(request):
    filetype = request.path_params['filetype']
    figure = Figure()
    figure.gca().plot(linspace(0, 1, 5), rand(5))
    buffer = BytesIO()
    figure.savefig(buffer, format=filetype)
    buffer.seek(0)
    return StreamingResponse(buffer)

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, subscription)

app = Application(routes=[
    Route('/figure.{filetype}', endpoint=figure)
], debug=True)

app.mount('/graphql', GraphQL(schema, debug=True))
