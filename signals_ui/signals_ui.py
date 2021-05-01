from common import Observable

from dearpygui.core import *
from dearpygui.simple import *

class SignalsUI(Observable):
    def __init__(self):
        super().__init__([
            'started',
            'stopped'
        ])

        set_start_callback(lambda: self.emit('started'))

        with window('Signals'):
            with node_editor('Signal Editor'):
                pass

    def signals_changed(self, signals):
        items = get_all_items()
        for signal in signals.values():
            if f'signal_{signal.id}' in items:
                continue

            with node(f'signal_{signal.id}', parent='Signal Editor'):
                pass

    def connections_changed(self, connections):
        pass

    async def start(self):
        start_dearpygui(primary_window='Signals')
        self.emit('stopped')
