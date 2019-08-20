from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from matplotlib.figure import Figure
from matplotlib.backends.backend_webagg_core import (
    FigureManagerWebAgg,
    new_figure_manager_given_figure
)

import json

class Measurement(object):
    def __init__(self, path):
        self.path = path
        self.figure = Figure()
        self.axis = self.figure.add_subplot(111)
        self.axis.plot([1, 2, 3, 4, 5], [1, 2, 3, 2, 1])
        self.figure_manager = new_figure_manager_given_figure(id(self.figure), self.figure)

class MainHandler(WebSocketHandler):
    def initialize(self):
        self.measurements = []
        self.supports_binary = True

    def open(self):
        pass

    def on_message(self, message):
        message = json.loads(message)

        if message['type'] == 'open_file':
            measurement = Measurement(message['value'])
            self.measurements.append(measurement)
            self.send_json({
                'type': 'open_file_success',
                'figure_id': measurement.figure_manager.num,
                'value': message['value']
            })
            measurement.figure_manager.add_web_socket(self)
            
        elif message['type'] == 'supports_binary':
            self.supports_binary = message['value']

        else:
            for measurement in self.measurements:
                if measurement.figure_manager.num == message['figure_id']:
                    measurement.figure_manager.handle_json(message)

    def on_close(self):
        pass

    def check_origin(self, origin):
        return True

    def send_json(self, content):
        self.write_message(json.dumps(content))

    def send_binary(self, blob):
        if self.supports_binary:
            self.write_message(blob, binary=True)
        else:
            data_uri = "data:image/png;base64,{0}".format(
                blob.encode('base64').replace('\n', ''))
            self.write_message(data_uri)

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

    app.listen(8888)
    IOLoop.current().start()
