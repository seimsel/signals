from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

import json

class MainHandler(WebSocketHandler):
    def open(self):
        print('Server opened', flush=True)

    def on_message(self, message):
        message = json.loads(message)

        print(message['type'], flush=True)
        print(message['value']['path'], flush=True)

    def on_close(self):
        print('Server closed', flush=True)

    def check_origin(self, origin):
        return True

if __name__ == '__main__':
    app = Application([
        (r'/', MainHandler)
    ])

    app.listen(8888)
    IOLoop.current().start()
