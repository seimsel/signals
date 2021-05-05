from signals.sinks.plot_sink_signal import PlotSinkSignal
from .connection import Connection
from common import Observable

import asyncio
import os
from queue import Full, Empty
from multiprocessing import Process, Queue

class Signals(Observable):
    def __init__(self):
        super().__init__()
        self._queue = None
        self._cwd = os.getcwd()
        self._process = None
        self._memory = None
        self._signals = {}
        self._connections = {}
        self._sink_ids = []

        self._signal_added = self.register_event('signal_added')
        self._signal_removed = self.register_event('signal_removed')
        self._connection_added = self.register_event('connection_added')
        self._connection_removed = self.register_event('connection_removed')
        self._data_changed = self.register_event('data_changed')

    @property
    def signals(self):
        return self._signals

    def add_signal(self, signal):
        signal.signals = self
        self._signals[signal.id] = signal

        if signal.category == 'Sinks':
            self._sink_ids.append(signal.id)

        self._signal_added(signal.id)
        self.restart()

    def remove_signal(self, id):
        del self._signals[id]
        self._signal_removed(id)
        self.restart()

    @property
    def connections(self):
        return self._connections

    def add_connection(self, connection):
        self._connections[connection.id] = connection
        self._connection_added(connection.id)
        self.restart()

    def add_connection(self, source_signal_id, output, sink_id, input):
        connection = Connection(source_signal_id, output, sink_id, input)
        self._connections[connection.id] = connection
        self._connection_added(connection.id)
        self.restart()

    def remove_connection(self, id):
        del self._connections[id]
        self._connection_removed(id)
        self.restart()

    @property
    def sinks(self):
        return [self.signals[id] for id in self._sink_ids]

    def _run(self, queue):
        os.chdir(self._cwd)
        async def process_all():
            while True:
                for signal in self.signals.values():
                    signal.data_ready = False

                for signal in self.sinks:
                    data = await process(signal)

                    if type(signal) == PlotSinkSignal:
                        try:
                            queue.put([
                                signal.id,
                                data
                            ])
                        except Full:
                            pass

        async def process(signal):
            input_connections = list(filter(
                lambda connection: connection.sink_id == signal.id,
                self.connections.values()
            ))
            
            for input_connection in input_connections:
                output_data = await process(self.signals[input_connection.source_id])
                signal.input_data[input_connection.input] = output_data[input_connection.output]


            output_data = await signal.output_data
            return output_data

        asyncio.run(process_all())

    def start(self):
        self._queue = Queue()
        self._process = Process(target=self._run, args=(self._queue,))
        self._process.start()

    def handle_process_events(self):
        try:
            signal_id, data = self._queue.get_nowait()
            self._data_changed(signal_id, data)
        except Empty:
            pass

    def restart(self):
        self.stop()
        self.start()

    def stop(self):
        if self._process:
            self._process.terminate()
            self._process.join()
            self._process.close()
