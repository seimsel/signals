from .source_signal import SourceSignal
from .connection import Connection
from common import Observable

from asyncio import get_event_loop
import numpy as np

class NotReady(Exception):
    pass

class Signals(Observable):
    def __init__(self):
        super().__init__()
        self._signals = {}
        self._signal_types = {}
        self._connections = {}

        self._request_process = self.register_event('request_process')
        self._signal_type_registered = self.register_event('signal_type_registered')
        self._signal_added = self.register_event('signal_added')
        self._signal_removed = self.register_event('signal_removed')
        self._connection_added = self.register_event('connection_added')
        self._connection_removed = self.register_event('connection_removed')

    def keys(self):
        return self._signals.keys()

    def values(self):
        return self._signals.values()

    def items(self):
        return self._signals.items()

    @property
    def signal_types(self):
        return self._signal_types

    def register_signal_type(self, signal_type):
        self._signal_types[signal_type.type_id] = signal_type
        self._signal_type_registered(signal_type.type_id)

    def __getitem__(self, item):
        return self._signals[item]

    def add_signal(self, signal):
        self._signals[signal.id] = signal
        self._signal_added(signal.id)
        signal.subscribe('request_process', self._request_process)
        signal.setup()

    def remove_signal(self, id):
        del self._signals[id]
        self._signal_removed(id)

    @property
    def leaves(self):
        sources = (connection.source_id for connection in self.connections)
        return filter(
            lambda signal: signal.id not in sources,
            self.values()
        )

    @property
    def connections(self):
        return self._connections

    def add_connection(self, connection):
        self._connections[connection.id] = connection
        self._connection_added(connection.id)
        self.restart()

    def add_connection(self, source_id, output, sink_id, input):
        connection = Connection(source_id, output, sink_id, input)
        self._connections[connection.id] = connection
        self._connection_added(connection.id)
        self.restart()

    def remove_connection(self, id):
        del self._connections[id]
        self._connection_removed(id)
        self.restart()

    def source_connections(self, signal_id):
        return filter(
            lambda connection: connection.source_id == signal_id,
            self._connections.values()
        )

    def process_all(self):
        output_data = {}

        for leaf in self.leaves:
            self._process(leaf, output_data)

        return output_data

    def _process(self, signal, output_data):
        if issubclass(type(signal), SourceSignal):
            output_data[signal.id] = signal.process()
            return

        for connection in self.source_connections(signal.id):
            output_data[connection.source_id] = self._process(
                self[connection.source_id]
            )

            output_data[signal.id] = signal.process(output_data[connection.source_id])
