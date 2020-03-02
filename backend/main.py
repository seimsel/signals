import re
import sys
import asyncio
import json
import numpy as np
import tornado.web
import tornado.websocket
import tornado.ioloop
import matplotlib.pyplot
import matplotlib.animation

from pathlib import Path
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backends.backend_webagg_core import (
    new_figure_manager_given_figure
)
from tornado.websocket import WebSocketClosedError

from drivers.lecroy_scope import LeCroyScope
from functions.moving_average import MovingAverage

matplotlib.pyplot.style.use(str(Path(__file__).with_name('dark.mplstyle')))

class Application(tornado.web.Application):
    class MatplotlibHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            self.instrument = LeCroyScope('10.1.11.79')
            self.functions = [
                MovingAverage()
            ]
            self.line = None
            self.figure = Figure()
            self.figure_id = 1
            self.figure_manager = new_figure_manager_given_figure(1, self.figure)
        
            self.timer = tornado.ioloop.PeriodicCallback(self.update, 1000/30, 0.1)
            self.timer.start()
            self.figure_manager.add_web_socket(self)

        def on_message(self, message):
            self.figure_manager.handle_json(json.loads(message))

        def on_close(self):
            self.figure_manager.remove_web_socket(self)

        def send_json(self, content):
            self.write_message(json.dumps(content))

        def send_binary(self, blob):
            self.write_message(blob, binary=True)

        def check_origin(self, origin):
            return True

        def update(self):
            wave_desc, wave_array_1 = self.instrument.read()

            for function in self.functions:
                wave_array_1 = function.process(wave_desc, wave_array_1)
                time_array = np.linspace(0, 1, len(wave_array_1))

            if not self.line:
                [self.line] = self.figure.gca().plot(time_array, wave_array_1)
            else:
                self.line.set_xdata(time_array)
                self.line.set_ydata(wave_array_1)

            try:
                self.send_json({
                    'type': 'refresh',
                    'figure_id': 1
                })
            except:
                self.timer.stop()

    def __init__(self):
        super().__init__([
            (r'/matplotlib', self.MatplotlibHandler)
        ])
        
if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    app = Application()
    app.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
