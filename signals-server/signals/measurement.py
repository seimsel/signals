from urllib.parse import urlparse
from .node import Node

class Measurement(Node):
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(self.url)
        super().__init__()

    @property
    def signals(self):
        return self.nodes
