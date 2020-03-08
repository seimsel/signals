from numpy import linspace, pi, sin
from numpy.random import rand
from scipy.signal import square

from channel import Channel
from parameters import FloatParameter, SelectParameter

functions = {
    'sine': sin,
    'square': square
}

class DemoChannel(Channel):
    def __init__(self, name, amplitude, function, frequency):
        super().__init__(name)

        self.function = SelectParameter('Function', function, functions.keys())
        self.amplitude = FloatParameter('Amplitude', amplitude)
        self.frequency = FloatParameter('Frequency', frequency)

        self.parameters = [
            self.function,
            self.amplitude,
            self.frequency
        ]

    @property
    def y(self):
        function = functions[self.function.value]
        f = self.frequency.value
        t = self.scope.t
        A = self.amplitude.value

        return (A*function(2*pi*f*t)
            + 0.1*A*rand(len(t)))
