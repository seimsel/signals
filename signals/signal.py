from uuid import uuid4

class Signal:
    def __init__(self):
        self.id = uuid4()
        self.inputs = None
        self._outputs = None

    async def process(self):
        raise NotImplementedError('A Signal needs to implement "process"')

    @property
    async def outputs(self):
        while self._outputs is None:
            self._outputs = await self.process()

        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        self._outputs = outputs
