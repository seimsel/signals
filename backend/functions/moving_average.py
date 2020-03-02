import numpy as np

class MovingAverage:
    def __init__(self, n = 128):
        self.params = {
            'n': 128
        }

    def process(self, wave_desc, wave_array_1):
        n = self.params['n']
        return np.convolve(wave_array_1, np.ones(n), 'valid') / n
