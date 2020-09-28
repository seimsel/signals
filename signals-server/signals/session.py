from .api_object import ApiObject
from .measurement_types.file_measurement import FileMeasurement

class Session(ApiObject):
    def __init__(self):
        super().__init__()
        self.measurements = []

    def measurement_with_url(self, measurement_url):
        for measurement in self.measurements:
            if measurement.url == measurement_url:
                return measurement

        measurement = FileMeasurement('file://test.csv')

        self.measurements = [
            measurement
        ]

        return FileMeasurement(measurement_url)
