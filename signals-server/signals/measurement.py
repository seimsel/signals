from .node import Node

class Measurement(Node):
    @property
    def view(self):
        return self.parent

    @property
    def channels(self):
        return self.children

    def appendChannel(self, channel):
        channel.measurement = self
        self.appendChild(channel)
