from signals import Signals, FileSourceSignal, GraphSinkSignal

from signals_ui import SignalsUI

if __name__ == '__main__':
    SIGNALS = Signals()
    SIGNALS_UI = SignalsUI(SIGNALS)

    SIGNALS.subscribe('signal_added', SIGNALS_UI.signal_added)
    SIGNALS.subscribe('signal_removed', SIGNALS_UI.signal_removed)
    SIGNALS.subscribe('signal_type_registered', SIGNALS_UI.signal_type_registered)

    SIGNALS.register_signal_type(FileSourceSignal)
    SIGNALS.register_signal_type(GraphSinkSignal)

    SIGNALS_UI.start()
