from .node import Node

class Measurement(Node):
    def __init__(self, url):
        super().__init__()
        self.url = url

    @property
    def channels(self):
        return self.children

    def appendChannel(self, channel):
        channel.measurement = self
        self.appendChild(channel)
