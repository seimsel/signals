from uuid import uuid4

class Signal:
    min_inputs = 1
    max_inputs = 64
    min_outputs = 1
    max_outputs = 64

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name
        self.input_descriptor = self.min_inputs
        self.output_descriptor = self.min_outputs
        self.inputs = []
        self._outputs = []

    def setup(self, signals):
        pass

    async def process(self):
        raise NotImplementedError('A Signal needs to implement "process"')

    @property
    async def outputs(self):
        while self._outputs == []:
            self._outputs = await self.process()

        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        self._outputs = outputs
