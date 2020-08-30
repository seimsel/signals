from .node import Node

class View(Node):
    @property
    def measurements(self):
        return self.children

    def appendMeasurement(self, measurement):
        self.appendChild(measurement)
