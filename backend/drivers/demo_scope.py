from numpy import linspace
from channels.demo import DemoChannel
from channels.moving_average import MovingAverageChannel
from scope import Scope

class DemoScope(Scope):
    def __init__(self, address):
        super().__init__(address)

        self.sample_frequency = 10e3
        self.sample_depth = 1000

        self.channel_types = [
            DemoChannel,
            MovingAverageChannel
        ]
