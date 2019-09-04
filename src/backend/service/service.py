from functools import wraps
from inspect import getargspec

from tornado.ioloop import IOLoop
from tornado.gen import coroutine

def method(f):
    @wraps(f)
    def withHooksAndEvents(self, *args, **kwargs):
        context = {
            'service': self,
            'method': f.__name__,
            'sid': kwargs.pop('sid', '0')
        }

        context.update(kwargs)

        for i, arg in enumerate(getargspec(f).args[1:]):
            if not arg in kwargs:
                context[arg] = args[i]

        self.applyHooks('before', context)
        result = f(self, *args, **kwargs)
        context['result'] = result
        self.applyHooks('after', context)

        for eventName, callbacks in self.callbacks.items():
            if f.__name__ in eventName:
                for callback in callbacks:
                    callback(self.name, eventName, result)

        return result

    return withHooksAndEvents

class Service():
    def __init__(self, app, name):
        self.app = app
        self.name = name
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

        @self.app.sio.on(name)
        def handle_events(sid, method, data={}):
            return getattr(self, method)(data, sid=sid)

    def applyHooks(self, moment, context):
        print(moment, context['method'], flush=True)
        for hook in self.hooks[moment][context['method']]:
            hook(context)

    def on(self, eventName, callback):
        if eventName == 'all':
            for eventName in self.callbacks.keys():
                self.callbacks[eventName].append(callback)
        else:
            self.callbacks[eventName].append(callback)

    def publish(self, eventName, room):
        def callback(name, eventName, data):
            IOLoop.current().add_callback(self.app.sio.emit, f'{name} {eventName}', data, room=room)

        self.on(eventName, callback)

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

