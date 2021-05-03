from .signal_editor import *
from .graph import *
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

        self._node_x = 100

        set_start_callback(lambda: self.emit('started'))
        set_key_press_callback(self._key_pressed)

        with window('Signals'):
            with tab_bar('Tab_Bar'):
                with tab('Graph'):
                    add_plot('Plot')
                with tab('Signal Editor'):
                    with node_editor('Node_Editor'):
                        pass

    def _key_pressed(self, sender, data):
        if data == 259:
            remove_selected_nodes(
                lambda node_id: self.emit('node_removed', node_id)
            )

    def signals_changed(self, signals):
        update_nodes(signals)

    def inputs_changed(self, signal):
        pass

    def outputs_changed(self, signal):
        pass

    def data_changed(self, signal, data):
        update_plot(signal, data)

    def connections_changed(self, connections):
        update_links(connections)

    async def start(self):
        show_debug()
        start_dearpygui(primary_window='Signals')
        self.emit('stopped')
