from ..signal import Signal
import numpy as np

class AdditionSignal(Signal):
    category = 'Basic Math'
    type_name = 'Addition'
    min_inputs = 2

    def process(self, input_data):
        output_data = {
            't': input_data.pop('t')
        }

        output_data['Out'] = np.sum(list(input_data.values()), axis=0)

        return output_data
