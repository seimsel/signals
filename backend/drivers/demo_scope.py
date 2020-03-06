from numpy import linspace, sin
from scipy.signal import square
from channels.demo import DemoChannel
from channels.moving_average import MovingAverageChannel

class DemoScope:
    def __init__(self):
        super().__init__()

        self.channels = []

        self.sample_frequency = 10e3
        self.sample_depth = 1000

        self._t = None
        self._t_needs_refresh = True

        self.add_channel(DemoChannel('Demo1', amplitude=1, function=square, frequency=100))
        self.add_channel(DemoChannel('Demo2', amplitude=1, function=sin, frequency=100))
        self.add_channel(MovingAverageChannel('MovingAverage1', source=self.channels[1], n=16))

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

    def get_channel_by_name(self, name):
        return next(filter(lambda channel: channel.name == name, self.channels))
