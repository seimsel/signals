from signals_ui import SignalsUI

from signals import (
    Signals,
    FileSourceSignal,
    AdditionSignal,
    GraphSinkSignal
)

import sys
from asyncio import get_event_loop

import signals_ui

def main(argv, signals, ui):
    file = FileSourceSignal()
    addition = AdditionSignal()
    graph = GraphSinkSignal()

    signals.add_signal(file)
    signals.add_signal(addition)
    signals.add_signal(graph)

    signals.add_connection(file.id, 0, addition.id, 0)
    signals.add_connection(file.id, 1, addition.id, 1)

    signals.add_connection(addition.id, 0, graph.id, 0)

    signals.subscribe('signals_changed', ui.signals_changed)
    signals.subscribe('connections_changed', ui.connections_changed)
    ui.subscribe('started', lambda: signals.emit('signals_changed', signals.signals))
    ui.subscribe('started', lambda: signals.emit('connections_changed', signals.connections))

    event_loop = get_event_loop()
    event_loop.create_task(signals.start())
    event_loop.create_task(ui.start())
    event_loop.run_forever()

if __name__ == '__main__':
    main(sys.argv, Signals(), SignalsUI())
