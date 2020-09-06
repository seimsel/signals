from .node import Node

class Signal(Node):
    def __init__(self, t, y, name):
        super().__init__()
        self.t = t
        self.y = y
        self.name = name
