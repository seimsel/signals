from common.observable import Observable
from uuid import uuid4

class Signal(Observable):
    type_id = str(uuid4())

    def __init__(self, name, **params):
        super().__init__()
        self._id = str(uuid4())
        self._params = params
        self._params['name'] = name

        self._parameter_changed = self.register_event('parameter_changed')
        self.request_process = self.register_event('request_process')

        self._ready = False

        self.subscribe('parameter_changed', self._on_parameter_changed)

    @property
    def id(self):
        return self._id

    def __getattr__(self, name):
        try:
            return self._params[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except KeyError:
            self._params[name] = value
            self._parameter_changed(name, value)

    def _on_parameter_changed(self, name, value):
        if name == 'name':
            return

        self.request_process()

    def setup(self):
        for name, value in self._params.items():
            if not value:
                continue

            self._parameter_changed(name, value)
