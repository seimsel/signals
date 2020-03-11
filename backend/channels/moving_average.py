from numpy import convolve, ones, zeros
from parameters import IntegerParameter, SelectParameter
from channel import Channel

class MovingAverageChannel(Channel):
    def __init__(self, name):
        super().__init__(name)
        
        self.source = SelectParameter('Source', None, [])
        self.n = IntegerParameter('n', 16)
        
        self.parameters = [
            self.n,
            self.source
        ]

    def was_added(self):
        channels = list(map(
            lambda channel: channel.name,
            self.scope.channels))

        self.source.options = channels

        if len(channels):
            self.source.value = channels[0]

    @property
    def y(self):
        if not self.source.value:
            return zeros(self.scope.sample_depth)

        source = self.scope.get_channel_by_name(self.source.value)

        return convolve(source.y, ones(self.n.value), 'same') / self.n.value

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
