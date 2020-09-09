from .api_object import ApiObject
from .window import Window
from .signal_types.basic_math import AdditionSignal

from .measurement_types.file_measurement import FileMeasurement

class Session(ApiObject):
    def __init__(self):
        super().__init__()
        initial_window = Window()

        measurement = FileMeasurement('file://test.csv')
        measurement.add_child(AdditionSignal([measurement.children[0], measurement.children[1]], 'Addition Maan'))
        initial_window.add_measurement(measurement)

        self.windows = [
            initial_window
        ]

    def measurement_with_id(self, measurement_id):
        measurement = None

        for window in self.windows:
            for measurement in window.measurements:
                if measurement.id == measurement_id:
                    return measurement
