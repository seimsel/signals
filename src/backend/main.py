from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from matplotlib.pyplot import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_webagg_core import (
    FigureManagerWebAgg,
    new_figure_manager_given_figure
)

from pathlib import Path

from uuid import uuid4
from urllib.parse import urlparse
import json
import csv
import numpy as np

class Channel():
    _data_changed = False
    _current_data = None

    @property
    def data_changed(self):
        return self._data_changed

    @property
    def current_data(self):
        self._data_changed = False
        return self._current_data

    @current_data.setter
    def current_data(self, data):
        self._current_data = data
        self._data_changed = True

class MathsChannel(Channel):
    def __init__(self, input_channels):
        self._input_channels = input_channels

    def process(self):
        raise NotImplementedError()

class AdditionChannel(MathsChannel):
    pass

class MainHandler(WebSocketHandler):
    def on_message(self, message):
        message = json.loads(message)

        if message['type'] == 'open_file':
            path = urlparse(message['value']).path

            data = None

            with open(path, newline='') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)
                data = np.array(list(reader))

            x = data.T[0]

            self.figure = Figure()
            self.figure_id = str(uuid4())
            axis = self.figure.add_subplot(111)
                        
            for y in data.T[1:]:
                axis.plot(x, y)

            self.figure_manager = new_figure_manager_given_figure(self.figure_id, self.figure)
            self.send_json({
                'type': 'open_file_success',
                'figure_id': self.figure_id,
                'value': message['value']
            })
            self.figure_manager.add_web_socket(self)
        else:
            self.figure_manager.handle_json(message)

    def check_origin(self, origin):
        return True

    def send_json(self, content):
        self.write_message(json.dumps(content))

    def send_binary(self, blob):
        self.write_message(blob, binary=True)

class MatplotlibHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/javascript')
        self.write(FigureManagerWebAgg.get_javascript())


if __name__ == '__main__':
    app = Application([
        (r'/', MainHandler),
        (r'/mpl.js', MatplotlibHandler),
        (r'/static/(.*)',
            StaticFileHandler,
            {'path': FigureManagerWebAgg.get_static_file_path()})
    ])

    style.use(str(Path(__file__).with_name('dark.mplstyle')))

    app.listen(8888)
    IOLoop.current().start()
