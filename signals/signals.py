from .connection import Connection
from common import Observable
from asyncio import get_running_loop, sleep

class Signals(Observable):
    def __init__(self):
        super().__init__()
        self._signals = {}
        self._connections = {}
        self._sink_ids = []

        self._signal_added = self.register_event('signal_added')
        self._signal_removed = self.register_event('signal_removed')
        self._connection_added = self.register_event('connection_added')
        self._connection_removed = self.register_event('connection_removed')

    @property
    def signals(self):
        return self._signals

    def add_signal(self, signal):
        signal.signals = self
        self._signals[signal.id] = signal

        if signal.category == 'Sinks':
            self._sink_ids.append(signal.id)

        self._signal_added(signal.id)
        signal.setup(self)

    def remove_signal(self, id):
        del self._signals[id]
        self._signal_removed(id)

    @property
    def connections(self):
        return self._connections

    def add_connection(self, connection):
        self._connections[connection.id] = connection
        self._connection_added(connection.id)

    def add_connection(self, source_signal_id, output, sink_id, input):
        connection = Connection(source_signal_id, output, sink_id, input)
        self._connections[connection.id] = connection
        self._connection_added(connection.id)

    def remove_connection(self, id):
        del self._connections[id]
        self._connection_removed(id)

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
                output_data = await process(self.signals[input_connection.source_id])
                signal.input_data[input_connection.input] = output_data[input_connection.output]

            return await signal.output_data

        while True:
            for signal in self.signals.values():
                signal.clear_data_ready()

            for signal in self.sinks:
                await process(signal)

            await sleep(0.01)

    def stop(self):
        get_running_loop().stop()
