from signals_ui import (
    SignalsUI,
    add_node
)

from signals import (
    Signals,
    FileSourceSignal,
    AdditionSignal,
    PlotSinkSignal
)

import sys
from asyncio import get_event_loop

class SignalsApplication:
    def __init__(self, argv):
        self.signals = Signals()
        self.ui = SignalsUI()

        self.signals.subscribe('signal_added', self._signal_added)
        self.signals.subscribe('signal_removed', self._signal_removed)
        self.signals.subscribe('connection_added', self._connection_added)
        self.signals.subscribe('connection_removed', self._connection_removed)

        self.ui.subscribe('started', self._ui_started)
        self.ui.subscribe('stopped', self.signals.stop)

    def _ui_started(self):
        file = FileSourceSignal('File_0')
        addition = AdditionSignal('Addition_0')
        graph = PlotSinkSignal('Graph_0')

        self.signals.add_signal(file)
        self.signals.add_signal(addition)
        self.signals.add_signal(graph)

        self.signals.add_connection(file.id, 0, addition.id, 0)
        self.signals.add_connection(file.id, 1, addition.id, 1)

        self.signals.add_connection(file.id, 0, graph.id, 0)
        self.signals.add_connection(file.id, 1, graph.id, 1)
        self.signals.add_connection(addition.id, 0, graph.id, 2)

    def _signal_added(self, id):
        signal = self.signals.signals[id]
        add_node(signal.id, signal.name)

    def _signal_removed(self, id):
        pass

    def _connection_added(self, id):
        pass

    def _connection_removed(self, id):
        pass

    def start(self):
        event_loop = get_event_loop()
        event_loop.create_task(self.signals.start())
        event_loop.create_task(self.ui.start())
        event_loop.run_forever()

if __name__ == '__main__':
    app = SignalsApplication(sys.argv)
    app.start()
