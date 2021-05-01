from ..signal import Signal

class AdditionSignal(Signal):
    category = 'Basic Math'
    type_name = 'Addition'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = [None] * 2

    async def process(self):
        output = self.inputs[0]

        for input in self.inputs[1:]:
            output += input

        return [output]
