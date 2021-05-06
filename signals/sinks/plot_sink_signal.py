from ..sink_signal import SinkSignal
from multiprocessing.queues import Queue

class PlotSinkSignal(SinkSignal):
    type_name = 'Plot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = 2
        self._queue = None

    @classmethod
    def setup(cls, signals):
        cls._data_changed = signals.register_event('data_changed')

    async def process(self, input_data):
        if not self._queue:
            self._queue = Queue()
