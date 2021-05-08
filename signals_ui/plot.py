from dearpygui.core import (
    add_line_series,
    add_plot
)

import numpy as np

def ui_add_plot():
    add_plot('plot')

def ui_update_plot(name, x, y):
    add_line_series('plot', name, x, y)
