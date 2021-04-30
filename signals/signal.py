class Signal:
    min_inputs = None
    max_inputs = None
    min_outputs = None
    max_outputs = None

    def __init__(self):
        self.subscriptions = {
            'parameter_changed': []
        }
        self.subscribe('parameter_changed', lambda _: self.process)
        self._parameters = []

    def add_parameter(self, parameter):
        parameter.signal = self
        self._parameters.append(parameter)

    @property
    def parameters(self):
        return self._parameters
    
    def process(self):
        pass

    def subscribe(self, event, callback):
        self.subscriptions[event].append(callback)

    def emit(self, event, payload):
        for callback in self.subscriptions[event]:
            callback(payload)
