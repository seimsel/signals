from .connection import Connection
from common import Observable

import numpy as np

import asyncio
import os
from multiprocessing import Process

class NotReady(Exception):
    pass

class Signals(Observable):
    def __init__(self):
        super().__init__()
        self._cwd = os.getcwd()
        self._signals = {}
        self._signal_types = []
        self._connections = {}

        self._signal_type_registered = self.register_event('signal_type_registered')
        self._signal_added = self.register_event('signal_added')
        self._signal_removed = self.register_event('signal_removed')
        self._connection_added = self.register_event('connection_added')
        self._connection_removed = self.register_event('connection_removed')

    def register_signal_type(self, signal_type):
        signal_type.setup(self)
        self._signal_types.append(signal_type)
        self._signal_type_registered(signal_type)

    @property
    def signals(self):
        return self._signals

    def add_signal(self, signal):
        self._signals[signal.id] = signal
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

    def add_connection(self, source_id, output, sink_id, input):
        connection = Connection(source_id, output, sink_id, input)
        self._connections[connection.id] = connection
        self._connection_added(connection.id)
        self.restart()

    def remove_connection(self, id):
        del self._connections[id]
        self._connection_removed(id)
        self.restart()

    def with_type(self, signal_type_name):
        return list(filter(
            lambda signal: type(signal).type_name == signal_type_name,
            self.signals.values()
        ))

    @property
    def sinks(self):
        return list(filter(
            lambda signal: signal.category == 'Sinks',
            self.signals.values()
        ))

    async def process_all(self):
        async def process(signal):
            connections = filter(
                lambda connection: connection.sink_id == signal.id,
                self.connections.values()
            )
            
            input_data = np.empty(signal.inputs)
            for connection in connections:
                source = self.signals[connection.source_id]
                output_data = await process(source)
                input_data[connection.input] = output_data[connection.output]

            if not input_data.any():
                raise NotReady

            return await signal.process(input_data)

        for sink in self.sinks:
            try:
                await process(sink)
            except NotReady:
                pass


