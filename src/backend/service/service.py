from functools import wraps
from inspect import getargspec
from uuid import uuid4

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

        for eventName, listeners in self.listeners.items():
            if f.__name__ in eventName:
                for listener in listeners:
                    listener['callback'](self.name, eventName, result)

        return result

    return withHooksAndEvents

class Service():
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.listeners = {
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
                'patch': [],
                'remove': []
            },
            'after': {
                'find': [],
                'get': [],
                'create': [],
                'update': [],
                'patch': [],
                'remove': []
            }
        }

        @self.app.sio.on(name)
        def handle_events(sid, method, data={}, *params):
            return getattr(self, method)(data, *params, sid=sid)

    def applyHooks(self, moment, context):
        for hook in self.hooks[moment][context['method']]:
            hook(context)

    def on(self, eventName, callback):
        if eventName == 'all':
            result = []
            for eventName in self.listeners.keys():
                uid = str(uuid4())
                result.append(uid)
                self.listeners[eventName].append({
                    'id': uid,
                    'callback': callback
                })

                return result
        else:
            uid = str(uuid4())
            self.listeners[eventName].append({
                    'id': uid,
                    'callback': callback
                })
            return [uid]

    def removeListener(self, uid):
        for eventName in self.listeners.keys():
            for i, listener in enumerate(self.listeners[eventName]):
                if listener['id'] == uid:
                    self.listeners[eventName].pop(i)

    def find(self, *params):
        raise NotImplementedError()

    def get(self, uid, *params):
        raise NotImplementedError()

    def create(self, data, *params):
        raise NotImplementedError()

    def update(self, uid, data, *params):
        raise NotImplementedError()

    def patch(self, uid, data, *params):
        raise NotImplementedError()

    def remove(self, uid, *params):
        raise NotImplementedError()

