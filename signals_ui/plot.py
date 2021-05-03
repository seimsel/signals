from dearpygui.core import (
    add_line_series,
    add_plot
)

import numpy as np

def ui_add_plot():
    add_plot('plot')

def update_plot(signal, data):
    outputs = range(0, len(data))

    x = np.arange(0, len(data[0])).astype(float)
    print(x)

    for output in outputs:
        print(data[output])
        add_line_series('Plot', f'{signal.name} O_{output}##graph_{signal.id}_O_{output}', x, data[output].astype(float))
