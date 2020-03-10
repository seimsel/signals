class Parameter:
    def __init__(self, name, initialValue):
        self.id = id(self)
        self.name = name
        self.value = initialValue

class IntegerParameter(Parameter):
    pass

class FloatParameter(Parameter):
    pass

class SelectParameter(Parameter):
    def __init__(self, name, initialValue, options):
        super().__init__(name, initialValue)
        self.options = options
