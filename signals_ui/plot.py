from dearpygui.core import *
from dearpygui.simple import *

import numpy as np

def update_plot(signal, data):
    outputs = range(0, len(data))

    x = np.arange(0, len(data[0])).astype(float)
    print(x)

    for output in outputs:
        print(data[output])
        add_line_series('Plot', f'{signal.name} O_{output}##graph_{signal.id}_O_{output}', x, data[output].astype(float))
