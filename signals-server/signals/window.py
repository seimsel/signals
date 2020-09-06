from .node import Node

class Window(Node):
    @property
    def measurements(self):
        return self.children

    def add_measurement(self, measurement):
        self.add_child(measurement)
