from ..signal import Signal
import numpy as np

class AdditionSignal(Signal):
    category = 'Basic Math'
    type_name = 'Addition'
    min_inputs = 2

    def process(self, input_data):
        output_data = input_data[0]

        for channel in self.input_data[1:]:
            output_data[1:] += channel[1:]

        return np.array([output_data])
