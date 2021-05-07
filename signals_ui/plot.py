from dearpygui.core import (
    add_line_series,
    add_plot
)

import numpy as np

def ui_add_plot():
    add_plot('plot')

def ui_update_plot(id, data):
    x = np.arange(0, len(data[0])).astype(float)

    for i, channel in enumerate(data[1:]):
        add_line_series('plot', f'Channel {i}##{id}', x, channel.astype(float))
