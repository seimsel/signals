from .node import Node

from urllib.parse import urlparse
from pathlib import Path

class Measurement(Node):
    def __init__(self, url):
        super().__init__(isRoot=True)
        self.url = url

    @property
    def name(self):
        parsed_url = urlparse(self.url)

        if parsed_url.path:
            return Path(parsed_url.path).name
        elif parsed_url.netloc:
            return parsed_url.netloc

        return self.url

    @property
    def channels(self):
        return self.children

    def appendChannel(self, channel):
        channel.measurement = self
        self.appendChild(channel)
