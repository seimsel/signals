from numpy import linspace, pi, sin
from numpy.random import rand
from scipy.signal import square
from channels.moving_average import MovingAverageChannel
from channels.digitize import DigitizeChannel
from scope import Scope
from channel import Channel
from parameters import FloatParameter, SelectParameter, IntegerParameter

functions = {
    'sine': sin,
    'square': square
}

class DemoChannel(Channel):
    def __init__(self):
        super().__init__()

        self.function = SelectParameter('Function', 'sine', functions.keys())
        self.amplitude = FloatParameter('Amplitude', 1)
        self.frequency = FloatParameter('Frequency', 100)
        self.p_sample_depth = IntegerParameter('Sample Depth', 1000)
        self.p_start_time = FloatParameter('Start Time', 0)
        self.p_end_time = FloatParameter('End Time', 0.1)

        self.parameters = [
            self.function,
            self.amplitude,
            self.frequency,
            self.p_sample_depth,
            self.p_start_time,
            self.p_end_time
        ]

    @property
    def y(self):
        function = functions[self.function.value]
        f = self.frequency.value
        A = self.amplitude.value

        self.sample_depth = self.p_sample_depth.value
        self.start_time = self.p_start_time.value
        self.end_time = self.p_end_time.value

        t = self.t

        return (A*function(2*pi*f*t)
            + 0.1*A*rand(len(t)))


class DemoScope(Scope):
    def __init__(self, address):
        super().__init__(address)

        self.channel_types = [
            DemoChannel,
            MovingAverageChannel,
            DigitizeChannel
        ]
