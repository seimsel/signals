from io import BytesIO
from pathlib import Path
from ariadne import load_schema_from_path, make_executable_schema, ObjectType, SubscriptionType
from ariadne.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware
from vxi11 import Instrument
from drivers.lecroy_scope import LeCroyScope
from matplotlib.figure import Figure
from matplotlib.pyplot import style
from numpy.random import rand
from numpy import linspace, frombuffer
from functions.moving_average import MovingAverage

subscription = SubscriptionType()

style.use(str(Path(__file__).with_name('dark.mplstyle')))

state = {
    'functions': [
        {
            'instrumentAddress': '10.1.11.79',
            'name': 'MovingAverage'
        },
        {
            'instrumentAddress': '10.1.11.79',
            'name': 'MovingAverage'
        }
    ]
}

@subscription.source('waveform')
async def waveform_generator(obj, info, instrumentAddress):
    figure = Figure()
    line = None
    scope = LeCroyScope(instrumentAddress)

    while True:
        wave_desc, wave_array_1 = scope.read()
        time_array = linspace(0, 1, len(wave_array_1))

        for function in state['functions']:
            if function['instrumentAddress'] == instrumentAddress:
                f = eval(function['name']+'()')
                time_array, wave_array_1 = f.process(wave_desc, time_array, wave_array_1)

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

        yield  {
            'figure': image.decode('utf-8')
        }

@subscription.field('waveform')
def waveform_resolver(waveform, info, instrumentAddress):
    return waveform

query = ObjectType('Query')

@query.field('functions')
def functions_resolver(query, info, instrumentAddress):
    print(state['functions'])
    return filter(lambda f: f['instrumentAddress'] == instrumentAddress, state['functions'])

type_defs = load_schema_from_path('./graphql')
schema = make_executable_schema(type_defs, query, subscription)

app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
