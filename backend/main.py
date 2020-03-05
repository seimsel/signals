from io import BytesIO
from pathlib import Path
from ariadne import load_schema_from_path, make_executable_schema, ObjectType, SubscriptionType
from ariadne.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware
from vxi11 import Instrument
from drivers.demo_scope import DemoScope
from matplotlib.figure import Figure
from matplotlib.pyplot import style
from numpy.random import rand
from numpy import linspace, frombuffer
from functions.moving_average import MovingAverage

subscription = SubscriptionType()

style.use(str(Path(__file__).with_name('dark.mplstyle')))

@subscription.source('waveform')
async def waveform_generator(obj, info, instrumentAddress):
    scope = DemoScope()
    figure = Figure()
    lines = {}

    while True:
        for channel in scope.channels:
            if not channel.active:
                if channel.name in lines:
                    del lines[channel.name]
                    continue

            if not channel.name in lines:
                lines[channel.name] = figure.gca().plot(scope.t, channel.y)[0]
            else:
                lines[channel.name].set_ydata(channel.y)

        buffer = BytesIO()
        figure.savefig(buffer, format='svg')
        buffer.seek(0)
        image = buffer.read()
        buffer.close()

        yield  {
            'figure': image.decode('utf-8')
        }

@subscription.field('waveform')
def waveform_resolver(waveform, info, instrumentAddress):
    return waveform

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, subscription)

app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
