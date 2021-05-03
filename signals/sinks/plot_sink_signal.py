from ..sink_signal import SinkSignal

class PlotSinkSignal(SinkSignal):
    type_name = 'Plot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = 3

    def setup(self, signals):
        self.plot_data_changed = signals.register_event('plot_data_changed')

    async def process(self):
        self.plot_data_changed(self.inputs)
