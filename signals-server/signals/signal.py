from .node import Node

class Signal(Node):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def signals(self):
        return self.children

    def appendSignal(self, signal):
        signal.measurement = self.measurement
        self.appendChild(signal)
