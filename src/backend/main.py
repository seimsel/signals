import csv
from pathlib import Path

import numpy as np
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

def add_sid(context):
    context['data']['sid'] = context['sid']

def import_csv(context):
    header = None
    data = None
    service = context['service']
    app = service.app
    path = Path(context['data']['path'])

    with open(str(path), newline='') as csvfile:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(csvfile.read(1024))
        csvfile.seek(0)
        has_header = sniffer.has_header(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        if has_header:
            header = next(reader)

        data = np.asarray(list(reader), dtype='float64')

    x = data.T[0]

    channelIds = []
    for i, y in enumerate(data.T[1:], start=1):
        channel = app.services['channels'].create({
            'name': header[i] if header else f'Channel {i}',
            'x': x,
            'y': y
        })
        channelIds.append(channel['id'])

    context['data']['name'] = path.name
    context['data']['channelIds'] = channelIds

def populate_channels(context):
    service = context['service']
    app = service.app

    context['result']['channels'] = []
    for uid in context['result']['channelIds']:
        context['result']['channels'].append(app.services['channels'].get(uid, 'id', 'name'))

def publish_to_sid(app, service, method, data, sid):
    IOLoop.current().add_callback(app.sio.emit, f'{service} {method}', data['id'], room=sid)

def main():
    define('port', default=3000, help='run on the given port', type=int)
    parse_command_line()

    sio = AsyncServer()

    app = Pope(sio)
    app.services['clients'] = MemoryService(app, 'clients')
    app.services['measurements'] = MemoryService(app, 'measurements')
    app.services['measurements'].hooks['before']['create'].append(add_sid)
    app.services['measurements'].hooks['before']['create'].append(import_csv)
    app.services['measurements'].hooks['after']['get'].append(populate_channels)

    app.services['channels'] = MemoryService(app, 'channels')

    @app.sio.event
    def connect(sid, env):
        def publish(service, method, data):
            if data['sid'] == sid:
                publish_to_sid(app, service, method, data, sid)

        listenerIds = app.services['measurements'].on('all', publish)
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
