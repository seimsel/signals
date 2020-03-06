from numpy import linspace, pi
from numpy.random import rand

class DemoChannel:
    def __init__(self, name, amplitude, function, frequency):
        self.name = name
        self.active = False

        self.amplitude = amplitude
        self.function = function
        self.frequency = frequency

    @property
    def y(self):
        return (self.amplitude*self.function(2*pi*self.frequency*self.scope.t)
            + 0.1*self.amplitude*rand(self.scope.sample_depth))
