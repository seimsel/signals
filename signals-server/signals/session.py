from .api_object import ApiObject
from .window import Window

from .measurement_types.file_measurement import FileMeasurement

class Session(ApiObject):
    def __init__(self):
        super().__init__()
        initial_window = Window()

        measurement = FileMeasurement('file://test.csv')
        initial_window.add_measurement(measurement)

        self.windows = [
            initial_window
        ]
