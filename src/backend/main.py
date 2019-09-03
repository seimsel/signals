from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from socketio import AsyncServer, get_tornado_handler

define('port', default=3000, help='run on the given port', type=int)

sio = AsyncServer()

@sio.on('connect')
async def on_connect(sid, environ):
    sio.emit('Hello', room=sid)

def main():
    parse_command_line()
    app = Application(
        [
            (r'/socket.io/', get_tornado_handler(sio)),
            (r'/(.*)', StaticFileHandler, {
                'path': 'static',
                'default_filename': 'index.html'})
        ]
    )
    app.listen(options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
