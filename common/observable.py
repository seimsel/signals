from functools import partial

class Observable:
    def __init__(self):
        self._subscriptions = {}

    def register_event(self, event):
        self._subscriptions[event] = []
        return partial(self._emit, event)

    def subscribe(self, event, callback):
        self._subscriptions[event].append(callback)

    def _emit(self, event, *args, **kwargs):
        for callback in self._subscriptions[event]:
            callback(*args, **kwargs)
