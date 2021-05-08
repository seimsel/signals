from signals_ui.plot import ui_update_plot
from signals import Signals, FileSourceSignal, AdditionSignal
from signals_ui import SignalsUI

import sys
from queue import Empty as QueueEmpty
from multiprocessing import Process, Queue
from time import sleep

class SignalsController:
    def __init__(self, queue):
        self._queue = queue

    def start(self):
        self._signals = Signals()

        self._signals.subscribe('signal_type_registered', self._signal_type_registered)
        self._signals.subscribe('signal_added', self._signal_added)
        self._signals.subscribe('request_process', self._process)

        self._signals.register_signal_type(FileSourceSignal)
        self._signals.register_signal_type(AdditionSignal)

        file = FileSourceSignal('File_0', path='example.csv')
        addition = AdditionSignal('Addition_0', path='example.csv')

        self._signals.add_signal(file)
        self._signals.add_signal(addition)
        self._signals.add_connection(file.id, 'Ch_1', addition.id, 1)
        self._signals.add_connection(file.id, 'Ch_2', addition.id, 2)

    def _process(self):
        output_data = {
            self._signals[signal_id].name:output_data
            for (signal_id, output_data)
            in self._signals.process_all().items()
        }
        self._queue.put(['data_changed', output_data])

    def _signal_type_registered(self, signal_type_id):
        signal_type = self._signals.signal_types[signal_type_id]
        self._queue.put(['signal_type_registered', {
            'id': signal_type_id,
            'name': signal_type.type_name,
            'category': signal_type.category
        }])

    def _signal_added(self, signal_id):
        signal = self._signals[signal_id]
        self._queue.put(['signal_added', {
            'id': signal_id,
            'name': signal.name
        }])

class UIController:
    def __init__(self, queue):
        self._queue = queue
        self._ui = SignalsUI()
        self._ui.subscribe('rendered', self._rendered)

    def _handle_event(self, event, payload):
        if event == 'data_changed':
            for signal_name, output_data in payload.items():
                t = output_data.pop('t')

                for channel_name, channel_data in output_data.items():
                    ui_update_plot(f'{signal_name}_{channel_name}', t, channel_data)

    def _rendered(self):
        try:
            self._handle_event(*self._queue.get_nowait())
        except QueueEmpty:
            pass

    def start(self):
        self._ui.start()

class SignalsApplication:
    def __init__(self, argv):
        pass

    def start(self):
        queue = Queue()
        signals_controller = SignalsController(queue)
        ui_controller = UIController(queue)
        process = Process(target=signals_controller.start)
        process.start()
        ui_controller.start()
        process.terminate()
        process.join()
        process.close()

if __name__ == '__main__':
    app = SignalsApplication(sys.argv)
    app.start()
