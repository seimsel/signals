from .node import Node

class Channel(Node):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def channels(self):
        return self.children

    def appendChannel(self, channel):
        channel.measurement = self.measurement
        self.appendChild(channel)
