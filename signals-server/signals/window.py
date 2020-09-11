from .node import Node

class Window(Node):
    def __init__(self):
        super().__init__()
        self.type = 'Signal'

    @property
    def measurements(self):
        return self.children

    def add_measurement(self, measurement):
        self.add_child(measurement)

    def remove_measurement(self, measurementId):
        self.remove_child(measurementId)
