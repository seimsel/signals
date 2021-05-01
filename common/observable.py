class Observable:
    def __init__(self, events):
        self._subscriptions = {}

        for event in events:
            self._subscriptions[event] = []

    def subscribe(self, event, callback):
        self._subscriptions[event].append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._subscriptions[event]:
            callback(*args, **kwargs)
