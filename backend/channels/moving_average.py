from numpy import convolve, ones
from parameters import IntegerParameter
from channel import Channel

class MovingAverageChannel(Channel):
    def __init__(self, name, source, n):
        super().__init__(name)
        
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
