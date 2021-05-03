from ..sink_signal import SinkSignal

class GraphSinkSignal(SinkSignal):
    type_name = 'Graph'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = [None] * 3

    async def process(self):
        outputs = self.inputs
        return outputs
