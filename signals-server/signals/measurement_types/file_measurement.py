from numpy import genfromtxt
from urllib.parse import urlparse, unquote
from pathlib import Path

from ..measurement import Measurement
from ..signal import Signal

class FileMeasurement(Measurement):
    scheme = 'file://'

    def __init__(self, url):
        super().__init__(url)

        if self.parsed_url.netloc:
            self.path = Path(unquote(self.parsed_url.netloc))
        else:
            raise Exception(f'Invalid url: {self.url}')

        data = genfromtxt(self.path, delimiter=',').T

        t = data[0]

        for i, y in enumerate(data[1:]):
            self.add_child(Signal(t, y, f'Signal {i}'))

    @property
    def name(self):
        return self.path.name
