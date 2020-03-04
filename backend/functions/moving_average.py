import numpy as np

class IntegerParam:
    def __init__(self, name, value, lower_limit=None, upper_limit=None):
        self.name = name
        self.value = value
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

class MovingAverage:
    def __init__(self):
        self.n = IntegerParam('n', 128, lower_limit=1)
        self.params = [
            self.n
        ]

    def process(self, wave_desc, time_array, wave_array_1):
        result = np.convolve(wave_array_1, np.ones(self.n.value), 'valid') / self.n.value
        return np.linspace(0, 1, len(result)), result
