from ..signal import Signal

class AdditionSignal(Signal):
    category = 'Basic Math'
    type_name = 'Addition'
    min_inputs = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = [None] * self.min_inputs

    async def process(self):
        output = self.inputs[0]

        for input in self.inputs[1:]:
            output += input

        return [output]
