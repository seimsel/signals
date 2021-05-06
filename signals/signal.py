from uuid import uuid4

class Signal:
    min_inputs = 1
    max_inputs = 64
    min_outputs = 1
    max_outputs = 64

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name
        self._inputs = self.min_inputs
        self.outputs = self.min_outputs
        self.input_data = None
        self._output_data = None
        self.data_ready = False

    @classmethod
    def setup(cls, signals):
        pass

    async def process(self):
        raise NotImplementedError('A Signal must implement "process"')

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    async def output_data(self):
        while self.data_ready == False:
            self._output_data = await self.process()

        return self._output_data

    @output_data.setter
    def output_data(self, output_data):
        self._output_data = output_data
