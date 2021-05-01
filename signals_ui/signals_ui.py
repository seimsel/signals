from common import Observable

from dearpygui.core import *
from dearpygui.simple import *

class SignalsUI(Observable):
    def __init__(self):
        super().__init__([
            'started',
            'stopped',
            'node_removed'
        ])

        set_start_callback(lambda: self.emit('started'))
        set_key_press_callback(self._key_pressed)

        with window('Signals'):
            with node_editor('Signal Editor'):
                pass

    def _key_pressed(self, sender, data):
        if data == 259:
            for node_id in get_selected_nodes('Signal Editor'):
                self.emit('node_removed', node_id[7:])

    def signals_changed(self, signals):
        items = get_all_items()
        for signal in signals.values():
            if f'signal_{signal.id}' in items:
                continue

            with node(f'signal_{signal.id}', parent='Signal Editor'):
                pass

        for item in items:
            if 'signal_' in item and f'{item[7:]}' not in signals.keys():
                delete_item(item)

    def connections_changed(self, connections):
        pass

    async def start(self):
        start_dearpygui(primary_window='Signals')
        self.emit('stopped')
