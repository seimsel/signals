from functools import wraps
from tornado.ioloop import IOLoop
from tornado.gen import coroutine

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
        def handle_events(sid, action, data={}):
            data['sid'] = sid
            return getattr(self, action)(data)

    def __getattribute__(self, name):
        attribute = super().__getattribute__(name)

        if name in ['find', 'get', 'create', 'update', 'patch', 'remove']:
            @wraps(attribute)
            def with_hooks(*args, **kwargs):

                context = {
                    'app': self.app
                }

                if name == 'create':
                    context['data'] = args[0]

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
                                callback(self.name, eventName, result)
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
