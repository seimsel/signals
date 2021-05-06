from dearpygui.core import (
    add_line_series,
    add_plot
)

import numpy as np

def ui_add_plot():
    add_plot('plot')

def ui_update_plot(data):
    print(data)
    return
    outputs = range(0, len(data))

    x = np.arange(0, len(data[0])).astype(float)

    for output in outputs:
        add_line_series('plot', f'{output}', x, data[output].astype(float))
