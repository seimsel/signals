from .node import Node
from .channel import Channel

from numpy import genfromtxt, arange

from urllib.parse import urlparse
from pathlib import Path

class Measurement(Node):
    def __init__(self, url):
        super().__init__(isRoot=True)
        self.url = url
        self.parsed_url = urlparse(self.url)

        if self.parsed_url.scheme == 'file':
            if self.parsed_url.path:
                self.path = Path(self.parsed_url.path)
            elif self.parsed_url.netloc:
                self.path = Path(self.parsed_url.netloc)
            else:
                raise Exception(f'Invalid url: {self.url}')

            for data in genfromtxt(self.path.resolve(), delimiter=',').T:
                self.appendChannel(Channel(arange(0, len(data)), data))
        else:
            raise NotImplementedError(f'The scheme: {self.parsed_url.scheme} is not supported.')

    @property
    def name(self):
        if self.parsed_url.scheme == 'file':
            return self.path

        return self.url

    @property
    def channels(self):
        return list(self.nodes.values())

    def appendChannel(self, channel):
        channel.measurement = self
        self.appendChild(channel)
