from io import BytesIO
from pathlib import Path
from ariadne import load_schema_from_path, make_executable_schema, ObjectType, SubscriptionType, InterfaceType
from ariadne.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware
from matplotlib.figure import Figure
from matplotlib.pyplot import style
from numpy.random import rand
from numpy import linspace, frombuffer

from drivers.demo_scope import DemoScope

subscription = SubscriptionType()

style.use(str(Path(__file__).with_name('dark.mplstyle')))

class State:
    instruments = {
        'scope1.demo': DemoScope()
    }

@subscription.source('waveform')
async def waveform_generator(obj, info, instrumentAddress):
    instrument = State.instruments[instrumentAddress]
    figure = Figure()
    lines = {}

    while True:
        for channel in instrument.channels:
            if not channel.active:
                if channel.name in lines:
                    del lines[channel.name]
                    continue

            if not channel.name in lines:
                lines[channel.name] = figure.gca().plot(instrument.t, channel.y)[0]
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

query = ObjectType('Query')

@query.field('instrument')
def instrument_resolver(query, info, address):
    instrument = State.instruments[address]
    return {
        'address': address,
        'channels': instrument.channels
    }

instrument = ObjectType('Instrument')

@instrument.field('channel')
def channel_resolver(instrument, info, name):
    instrument = State.instruments[instrument['address']]
    channel = instrument.get_channel_by_name(name)
    return channel

channel = ObjectType('Channel')

@channel.field('parameter')
def parameter_resolver(channel, info, name):
    return channel.get_parameter_by_name(name)

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, query, instrument, channel, subscription)

app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
