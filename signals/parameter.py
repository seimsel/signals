class Parameter:
    def __init__(self, name):
        self.name = name
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.signal.emit('parameter_changed', self)
