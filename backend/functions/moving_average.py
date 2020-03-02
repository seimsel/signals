import numpy as np

class MovingAverage:
    def __init__(self, n = 128):
        self.n = n

    def process(self, wave_desc, wave_array_1):
        return np.convolve(wave_array_1, np.ones(self.n), 'valid') / self.n
