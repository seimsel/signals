from .node_editor import ui_add_node_editor
from common import Observable

from dearpygui.core import (
    start_dearpygui,
    set_start_callback,
    set_key_press_callback
)
from dearpygui.simple import (
    window,
    tab_bar,
    tab
)

class SignalsUI(Observable):
    def __init__(self):
        super().__init__()

        self._started = self.register_event('started')
        self._stopped = self.register_event('stopped')

        set_start_callback(lambda: self._started())
        set_key_press_callback(self._key_pressed)

        with window('Signals'):
            with tab_bar('Tab_Bar'):
                with tab('Plot'):
                    pass
                with tab('Signal Editor'):
                    ui_add_node_editor()

    def _key_pressed(self, sender, data):
        pass

    async def start(self):
        start_dearpygui(primary_window='Signals')
        self._stopped()
