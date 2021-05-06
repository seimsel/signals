from signals_ui import (
    SignalsUI,
    NodeAttribute,
    ui_add_node_type,
    ui_add_node,
    ui_add_node_link,
    ui_update_plot
)

from signals import Signals, FileSourceSignal, AdditionSignal, PlotSinkSignal

import os
import sys
import asyncio
from multiprocessing import Process

class SignalsApplication:
    def __init__(self, argv):
        self.signals = Signals()
        self.ui = SignalsUI()

        self._process = None

        self.signals.register_signal_type(FileSourceSignal)
        self.signals.register_signal_type(AdditionSignal)
        self.signals.register_signal_type(PlotSinkSignal)

        self.signals.subscribe('signal_type_registered', self._signal_type_registered)
        self.signals.subscribe('signal_added', self._signal_added)
        self.signals.subscribe('signal_removed', self._signal_removed)
        self.signals.subscribe('connection_added', self._connection_added)
        self.signals.subscribe('connection_removed', self._connection_removed)
        self.signals.subscribe('data_changed', self._data_changed)

        self.ui.subscribe('started', self._ui_started)
        self.ui.subscribe('rendered', self.signals.handle_process_events)
        self.ui.subscribe('link_added', self._ui_link_added)
        self.ui.subscribe('stopped', self.signals.stop)

    def _signal_type_registered(self, signal_type):
        def on_add_node():
            type_name = signal_type.type_name
            number = len(self.signals.with_type(signal_type.type_name))

            self.signals.add_signal(signal_type(f'{type_name}_{number}'))

        ui_add_node_type(signal_type.category, signal_type.type_name, on_add_node=on_add_node)

    def _signal_added(self, id):
        signal = self.signals.signals[id]
        attributes = []

        inputs = signal.inputs

        if type(inputs) == int:
            inputs = range(0, inputs)

        for input in inputs:
            if type(input) == int:
                input = f'I_{input}'

            attributes.append(NodeAttribute(input, type='input'))

        outputs = signal.outputs

        if type(outputs) == int:
            outputs = range(0, outputs)

        for output in outputs:
            if type(output) == int:
                output = f'O_{output}'

            attributes.append(NodeAttribute(output, type='output'))
        

        ui_add_node(signal.id, signal.name, attributes)

    def _signal_removed(self, id):
        pass

    def _connection_added(self, id):
        connection = self.signals.connections[id]

        # ui_add_node_link(
        #     connection.source_id,
        #     f'O_{connection.output}',
        #     connection.sink_id,
        #     f'I_{connection.input}'
        # )

    def _connection_removed(self, id):
        pass

    def _ui_link_added(self, source_id, source_attribute_name, sink_id, sink_attribute_name):
        output = int(source_attribute_name[2:])
        input = int(sink_attribute_name[2:])

        self.signals.add_connection(source_id, output, sink_id, input)

    def _data_changed(self, signal_id, data):
        ui_update_plot(data)

    def _ui_started(self):
        self._start_processing()

    def start(self):
        self.ui.start()
        
    def _run(self):
        os.chdir(self._cwd)
        asyncio.run(self.process_all())

    def _start_processing(self):
        self._process = Process(target=self._run)
        self._process.start()

    def _restart_processing(self):
        self._stop_processing()
        self._start_processing()

    def _stop_processing(self):
        if self._process:
            self._process.terminate()
            self._process.join()
            self._process.close()

if __name__ == '__main__':
    app = SignalsApplication(sys.argv)
    app.start()
