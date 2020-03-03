from io import BytesIO
from asyncio import sleep
from base64 import b64encode
from pathlib import Path
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette as Application
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount
from starlette.responses import StreamingResponse
from ariadne import SubscriptionType
from vxi11 import Instrument
from drivers.lecroy_scope import LeCroyScope
from matplotlib.figure import Figure
from matplotlib.pyplot import style
from numpy.random import rand
from numpy import linspace, frombuffer

subscription = SubscriptionType()

style.use(str(Path(__file__).with_name('dark.mplstyle')))

@subscription.source('scope')
async def scope_generator(obj, info, address):
    figure = Figure()
    line = None
    scope = LeCroyScope(address)

    while True:
        wave_desc, wave_array_1 = scope.read()
        time_array = linspace(0, 1, len(wave_array_1))

        if not line:
            [line] = figure.gca().plot(time_array, wave_array_1)
        else:
            line.set_xdata(time_array)
            line.set_ydata(wave_array_1)

        buffer = BytesIO()
        figure.savefig(buffer, format='svg')
        buffer.seek(0)
        image = buffer.read()
        buffer.close()

        yield {
            'channels': [
                {
                    'waveform': {
                        'figure': image.decode('utf-8')
                    }
                }
            ]
        }

@subscription.field('scope')
def scope_resolver(scope, info, address):
    return scope

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, subscription)

routes = [
    Mount('/graphql', GraphQL(schema, debug=True)),
    Mount('/app', StaticFiles(directory='../frontend/dist', html=True))
]

app = Application(routes=routes, debug=True)
