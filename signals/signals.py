from .connection import Connection
from common import Observable
from asyncio import get_running_loop, sleep

class Signals(Observable):
    def __init__(self):
        super().__init__([
            'signals_changed',
            'inputs_changed',
            'connections_changed',
            'data_changed'
        ])
        self._signals = {}
        self._connections = {}
        self._sink_ids = []

    @property
    def signals(self):
        return self._signals

    def add_signal(self, signal):
        signal.signals = self
        self._signals[signal.id] = signal

        if signal.category == 'Sinks':
            self._sink_ids.append(signal.id)

        self.emit('signals_changed', self.signals)

    def remove_signal(self, id):
        del self._signals[id]
        self.emit('signals_changed', self.signals)

    @property
    def connections(self):
        return self._connections

    def add_connection(self, connection):
        self._connections[connection.id] = connection
        self.emit('connections_changed', self.connections)

    def add_connection(self, source_signal_id, output, sink_id, input):
        connection = Connection(source_signal_id, output, sink_id, input)
        self._connections[connection.id] = connection
        self.emit('connections_changed', self.connections)

    def remove_connection(self, id):
        del self._connections[id]
        self.emit('connections_changed', self.connections)

    @property
    def sinks(self):
        return [self.signals[id] for id in self._sink_ids]

    async def start(self):
        async def process(signal):
            input_connections = list(filter(
                lambda connection: connection.sink_id == signal.id,
                self.connections.values()
            ))
            
            for input_connection in input_connections:
                outputs = await process(self.signals[input_connection.source_id])
                signal.inputs[input_connection.input] = outputs[input_connection.output]

            return await signal.outputs

        while True:
            for signal in self.signals.values():
                signal.outputs = []

            for signal in self.sinks:
                data = await process(signal)
                self.emit('data_changed', signal, data)

            await sleep(0.01)

    def stop(self):
        get_running_loop().stop()
