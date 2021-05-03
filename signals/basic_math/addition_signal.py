from ..signal import Signal

class AdditionSignal(Signal):
    category = 'Basic Math'
    type_name = 'Addition'
    min_inputs = 2

    async def process(self):
        output_data = self.input_data[0]

        for channel in self.input_data[1:]:
            output_data += channel

        self.data_ready = True
        return [output_data]
