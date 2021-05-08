from dearpygui.core import (
    add_line_series,
    add_plot
)

import numpy as np

def ui_add_plot():
    add_plot('plot')

def ui_update_plot(id, input_data):
    t = input_data.pop('t')

    for channel_name, channel_data in input_data.items():
        add_line_series('plot', f'{channel_name}##{id}', t, channel_data.astype(float))
