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
from argparse import ArgumentParser

from uuid import uuid4
from urllib.parse import urlparse
import json
import csv
import numpy as np

class Channel():
    def __init__(self):
        self._data_changed = False
        self._current_data = None

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
    def __init__(self):
        self.sources = []

    def process(self):
        raise NotImplementedError()

class AdditionChannel(MathsChannel):
    def process(self):
        x1, y1 = self.sources[0]._current_data
        y_result = np.copy(y1)

        for channel in self.sources[1:]:
            _, y = channel._current_data
            y_result += y

        self.current_data = (x1, y_result)

class Measurement():
    def __init__(self):
        self.channels = []

    @classmethod
    def from_csv(cls, path):
        measurement = Measurement()

        with open(path, newline='') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            data = np.asarray(list(reader), dtype='float64')

        x = data.T[0]
        
        for y in data.T[1:]:
            channel = Channel()
            channel.current_data = (x, y)
            measurement.channels.append(channel)

        return measurement

    @staticmethod
    def plot(measurement, axis):
        for channel in measurement.channels:
            x, y = channel.current_data
            axis.plot(x, y)

class MainHandler(WebSocketHandler):
    def on_message(self, message):
        message = json.loads(message)

        if message['type'] == 'open_file':
            path = urlparse(message['value']).path

            self.measurement = Measurement.from_csv(path)

            additionChannel = AdditionChannel()
            additionChannel.sources = self.measurement.channels[0:2]
            additionChannel.process()
            self.measurement.channels.append(additionChannel)

            self.figure = Figure()
            self.figure_id = str(uuid4())
            axis = self.figure.add_subplot(111)
                        
            Measurement.plot(self.measurement, axis)

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
    argumentParser = ArgumentParser()
    argumentParser.add_argument('--port', dest='port', type=int)
    args = argumentParser.parse_args()

    app = Application([
        (r'/', MainHandler),
        (r'/mpl.js', MatplotlibHandler),
        (r'/static/(.*)',
            StaticFileHandler,
            {'path': FigureManagerWebAgg.get_static_file_path()})
    ])

    style.use(str(Path(__file__).with_name('dark.mplstyle')))

    app.listen(args.port)
    IOLoop.current().start()
