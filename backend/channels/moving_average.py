from numpy import convolve, ones

class IntegerParameter:
    def __init__(self, name, initialValue):
        self.name = name
        self.value = initialValue

class MovingAverageChannel:
    def __init__(self, name, source, n):
        self.name = name
        self.active = False
        
        self.source = source
        self.n = IntegerParameter('n', n)
        
        self.parameters = [
            self.n
        ]

    @property
    def y(self):
        return convolve(self.source.y, ones(self.n.value), 'same') / self.n.value

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
