from numpy import convolve, ones

class MovingAverageChannel:
    def __init__(self, name, source, n):
        self.name = name
        self.active = False
        
        self.source = source
        self.n = n

    @property
    def y(self):
        return convolve(self.source.y, ones(self.n), 'same') / self.n
