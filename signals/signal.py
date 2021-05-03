from uuid import uuid4

class Signal:
    min_inputs = 1
    max_inputs = 64
    min_outputs = 1
    max_outputs = 64

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name
        self.inputs = self.min_inputs
        self.outputs = self.min_outputs
        self.input_data = None
        self._output_data = None
        self._data_ready = False

    def setup(self, signals):
        pass

    def clear_data_ready(self):
        self._data_ready = False

    async def process(self):
        self._data_ready = True

    @property
    async def output_data(self):
        while self._data_ready == False:
            self._output_data = await self.process()

        return self._output_data

    @output_data.setter
    def output_data(self, output_data):
        self._output_data = output_data
