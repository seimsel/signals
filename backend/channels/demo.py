from numpy import linspace, pi, sin
from numpy.random import rand
from scipy.signal import square

from channel import Channel
from parameters import SelectParameter

functions = {
    'sine': sin,
    'square': square
}

class DemoChannel(Channel):
    def __init__(self, name, amplitude, function, frequency):
        super().__init__(name)

        self.amplitude = amplitude
        self.function = SelectParameter('Function', function, functions.keys())
        self.frequency = frequency

        self.parameters = [
            self.function
        ]

    @property
    def y(self):
        return (self.amplitude*functions[self.function.value](2*pi*self.frequency*self.scope.t)
            + 0.1*self.amplitude*rand(self.scope.sample_depth))
