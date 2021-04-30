class Signals:
    def __init__(self, signals=[], signal_types=[]):
        self._signals = signals
        self._signal_types = signal_types
        self.subscriptions = {
            'signal_type_registered': [],
            'parameter_type_registered': [],
            'signal_added': [],
            'signal_removed': []
        }

    def register_signal_type(self, signal_type):
        self._signal_types.append(signal_type)
        self.emit('signal_type_registered', signal_type)

    def subscribe(self, event, callback):
        self.subscriptions[event].append(callback)

    def emit(self, event, payload):
        for callback in self.subscriptions[event]:
            callback(payload)

    def add_signal(self, signal):
        n = sum(1 for _ in filter(
            lambda s: s.type_name == signal.type_name,
            self._signals
        ))

        signal.name = f'{signal.type_name}_{n}'
        self._signals.append(signal)
        self.emit('signal_added', signal)

    def remove_signal(self, signal_name):
        signal = next(filter(
            lambda s: s.name == signal_name,
            self._signals
        ))

        self._signals.remove(signal)

        self.emit('signal_removed', signal)

    @property
    def sources(self):
        return list(filter(
            lambda s: s.category == 'Sources',
            self._signals
        ))
