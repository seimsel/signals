from ..sink_signal import SinkSignal

class PlotSinkSignal(SinkSignal):
    type_name = 'Plot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = 3

    async def process(self):
        self.data_ready = True
        return self.input_data
