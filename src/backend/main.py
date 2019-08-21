from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from matplotlib.figure import Figure
from matplotlib.backends.backend_webagg_core import (
    FigureManagerWebAgg,
    new_figure_manager_given_figure
)

from uuid import uuid4
import json

class MainHandler(WebSocketHandler):
    def on_message(self, message):
        message = json.loads(message)

        if message['type'] == 'open_file':
            self.figure = Figure()
            self.figure_id = str(uuid4())
            axis = self.figure.add_subplot(111)
            axis.plot([1,2,3,2,1])
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

    app.listen(8888)
    IOLoop.current().start()
