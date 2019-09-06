from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from socketio import AsyncServer, get_tornado_handler

from service.memoryservice import MemoryService

class Pope(Application):
    def __init__(self, sio):
        self.services = {}
        self.sio = sio
        super().__init__([
            (r'/socket.io/', get_tornado_handler(self.sio)),
            (r'/(.*)', StaticFileHandler, {
                'path': 'static',
                'default_filename': 'index.html'})
        ])

def populateSid(context):
    context['data']['sid'] = context['sid']

def publishToSid(app, service, method, data, sid):
    IOLoop.current().add_callback(app.sio.emit, f'{service} {method}', data, room=sid)

def main():
    define('port', default=3000, help='run on the given port', type=int)
    parse_command_line()

    sio = AsyncServer()

    app = Pope(sio)
    app.services['clients'] = MemoryService(app, 'clients')
    app.services['measurements'] = MemoryService(app, 'measurements')
    app.services['measurements'].hooks['before']['create'].append(populateSid)

    @app.sio.event
    def connect(sid, env):
        def publish(service, method, data):
            if data['sid'] == sid:
                publishToSid(app, service, method, data, sid)

        listenerIds = app.services['measurements'].on('created', publish)
        app.services['clients'].create({
            'sid': sid,
            'listenerIds': listenerIds
        })

    @app.sio.event
    def disconnect(sid):
        client = app.services['clients'].find(lambda client: client['sid'] == sid)[0]
        for listenerId in client['listenerIds']:
            app.services['measurements'].removeListener(listenerId)

    app.listen(options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
