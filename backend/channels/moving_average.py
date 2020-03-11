from numpy import convolve, ones, zeros
from parameters import IntegerParameter, SourceParameter
from channel import Channel

class MovingAverageChannel(Channel):
    def __init__(self):
        super().__init__()
        
        self.source = SourceParameter('Source', self)
        self.n = IntegerParameter('n', 16)
        
        self.parameters = [
            self.n,
            self.source
        ]

    @property
    def y(self):
        source = self.scope.get_channel_by_name(self.source.value)
        t, y = source.data
        self.start_time = source.start_time
        self.end_time = source.end_time
        self.sample_depth = source.sample_depth

        return convolve(y, ones(self.n.value), 'same') / self.n.value

    def get_parameter_by_name(self, name):
        return next(filter(lambda parameter: parameter.name == name, self.parameters))
