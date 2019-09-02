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
from functools import wraps
from operator import itemgetter

class Service():
    def __init__(self, app):
        self.app = app
        self.items = []
        self.callbacks = {
            'created': [],
            'updated': [],
            'patched': [],
            'removed': []
        }
        self.hooks = {
            'before': {
                'find': [],
                'get': [],
                'create': [],
                'update': [],
                'patche': [],
                'remove': []
            },
            'after': {
                'find': [],
                'get': [],
                'create': [],
                'update': [],
                'patche': [],
                'remove': []
            }
        }

    def __getattribute__(self, name):
        attribute = super().__getattribute__(name)

        if name in ['find', 'get', 'create', 'update', 'patch', 'remove']:
            @wraps(attribute)
            def with_hooks(*args, **kwargs):
                if name == 'create':
                    context = {
                        'app': self.app,
                        'data': args[0]
                    }
                else:
                    context = {}

                for hook in self.hooks['before'][name]:
                    hook(context)

                if name == 'get':
                    result = attribute(args[0])
                elif name == 'create':
                    result = attribute(context['data'])
                else:
                    result = attribute()

                context = {
                    'app': self.app,
                    'result': result
                }

                for hook in self.hooks['after'][name]:
                    hook(context)

                return result
                
            if name in ['create', 'update', 'patch', 'remove']:
                @wraps(with_hooks)
                def with_callbacks(*args, **kwargs):
                    result = with_hooks(*args, **kwargs)
                    for eventName, callbacks in self.callbacks.items():
                        for callback in callbacks:
                            if name in eventName:
                                callback(eventName, result)
                    return result

                return with_callbacks
            
            return with_hooks

        return attribute

    def on(self, eventName, callback):
        if eventName == 'all':
            for eventName in self.callbacks.keys():
                self.callbacks[eventName].append(callback)
        else:
            self.callbacks[eventName].append(callback)

    def find(self, *params):
        raise NotImplementedError()

    def get(self, id, *params):
        raise NotImplementedError()

    def create(self, data, *params):
        raise NotImplementedError()

    def update(self, id, data, *params):
        raise NotImplementedError()

    def patch(self, id, data, *params):
        raise NotImplementedError()
    
    def remove(self, id, *params):
        raise NotImplementedError()

class MemoryService(Service):
    def find(self, *params):
        return self.items

    def get(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return item

    def create(self, data, *params):
        item = {
            'id': str(uuid4()),
            **data
        }
        self.items.append(item)

        return item

    def update(self, id, data, *params):
        for i, item in enumerate(self.items):
            if item['id'] == id:
                self.items[i] = {
                    'id': id,
                    **data
                }

                return item

    def patch(self, id, data, *params):
        for item in self.items:
            if item['id'] == id:
                return item.update(data)
    
    def remove(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return self.items.remove(item)

class MainHandler(WebSocketHandler):
    def open(self):
        self.application.services['measurements'].on('created', lambda e, d: self.write_message({
            'service': 'measurements',
            'action': 'created',
            'data': {
                'path': d['path'],
                'figure': d['figure']
            }
        }))

    def on_message(self, message):
        service, action, data = itemgetter('service', 'action', 'data')(json.loads(message))
        getattr(self.application.services[service], action)(data)

    def check_origin(self, origin):
        return True

class MatplotlibHandler(WebSocketHandler):
    def initialize(self):
        self.figure_manager = None

    def on_message(self, message):
        message = json.loads(message)

        if not self.figure_manager:
            self.figure_manager = new_figure_manager_given_figure(
                message['figure_id'],
                self.application.services['figures'].get(message['figure_id'])['handle']
            )
            self.figure_manager.add_web_socket(self)
        
        self.figure_manager.handle_json(message)

    def send_json(self, content):
        self.write_message(json.dumps(content))

    def send_binary(self, blob):
        self.write_message(blob, binary=True)

    def check_origin(self, origin):
        return True

class Pope(Application):
    def __init__(self, handlers=None, default_host=None, transforms=None, **settings):
        self.services = {}
        super().__init__(handlers, default_host, transforms, **settings)

def create_channels_from_url(context):
    with open(urlparse(context['data']['path']).path, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        data = np.asarray(list(reader), dtype='float64')

    x = data.T[0]
    
    channels = []
    for i, y in enumerate(data.T[1:]):
        ch = context['app'].services['channels'].create({
            'name': f'Channel {i}',
            'kind': 'source',
            'type': 'csv',
            'current_data': {
                'x': x,
                'y': y
            }
        })

        channels.append(ch['id'])

    context['data']['channels'] = channels

def create_figure(context):
    handle = Figure()
    figure = context['app'].services['figures'].create({
        'handle': handle,
        'axis': handle.add_subplot(111)
    })

    context['data']['figure'] = figure['id']

def plot(context):
    figure = context['app'].services['figures'].get(context['result']['figure'])
    for ch in context['app'].services['channels'].find():
        figure['axis'].plot(ch['current_data']['x'], ch['current_data']['y'])

if __name__ == '__main__':
    argumentParser = ArgumentParser()
    argumentParser.add_argument('--port', dest='port', type=int)
    args = argumentParser.parse_args()

    app = Pope([
        (r'/', MainHandler),
        (r'/matplotlib', MatplotlibHandler)
    ])

    app.services['measurements'] = MemoryService(app)
    app.services['figures'] = MemoryService(app)
    app.services['channels'] = MemoryService(app)

    app.services['measurements'].hooks['before']['create'] = [
        create_channels_from_url,
        create_figure
    ]

    app.services['measurements'].hooks['after']['create'] = [
        plot
    ]

    style.use(str(Path(__file__).with_name('dark.mplstyle')))

    app.listen(args.port)
    IOLoop.current().start()
