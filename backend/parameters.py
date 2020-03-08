class Parameter:
    def __init__(self, name, initialValue):
        self.name = name
        self.value = initialValue

class IntegerParameter(Parameter):
    def __init__(self, name, initialValue):
        super().__init__(name, initialValue)

class SelectParameter(Parameter):
    def __init__(self, name, initialValue, options):
        super().__init__(name, initialValue)
        self.options = options
