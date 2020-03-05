from numpy import linspace, pi, sin
from numpy.random import rand
from scipy.signal import square

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

class DemoScope:
    def __init__(self):
        super().__init__()

        self.channels = []

        self.sample_frequency = 10e3
        self.sample_depth = 1000

        self._t = None
        self._t_needs_refresh = True

        self.add_channel(DemoChannel('C1', amplitude=1, function=square, frequency=100)) 
        self.add_channel(DemoChannel('C2', amplitude=1, function=sin, frequency=100)) 

        for channel in self.channels:
            channel.active = True

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name in ['sample_frequency', 'sample_depth']:
            self._t_needs_refresh = True

    @property
    def t(self):
        if self._t_needs_refresh:
            self._t = linspace(0,
                self.sample_depth/self.sample_frequency,
                self.sample_depth)
        
        return self._t

    def add_channel(self, channel):
        channel.scope = self
        self.channels.append(channel)
