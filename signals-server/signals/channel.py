from .node import Node

class Channel(Node):
    @property
    def channels(self):
        return self.children

    def appendChannel(self, channel):
        channel.measurement = self.measurement
        self.appendChild(channel)
