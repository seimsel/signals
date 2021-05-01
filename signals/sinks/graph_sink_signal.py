from ..sink_signal import SinkSignal

class GraphSinkSignal(SinkSignal):
    type_name = 'Graph'

    def __init__(self):
        super().__init__()
        self.inputs = [None]

    async def process(self):
        outputs = self.inputs
        return outputs
