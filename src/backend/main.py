from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

class MainHandler(WebSocketHandler):
    def open(self):
        print('Server opened')

    def on_message(self, message):
        print(message)

    def on_close(self):
        print('Server closed')

    def check_origin(self, origin):
        return True

if __name__ == '__main__':
    app = Application([
        (r'/', MainHandler)
    ])

    app.listen(8888)
    IOLoop.current().start()
