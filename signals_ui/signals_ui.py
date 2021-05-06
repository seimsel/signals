from .plot import ui_add_plot
from .node_editor import ui_add_node_editor
from common import Observable

from dearpygui.core import (
    set_render_callback,
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
        self._link_added = self.register_event('link_added')
        self._rendered = self.register_event('rendered')

        set_start_callback(lambda: self._started())
        set_render_callback(lambda: self._rendered())
        set_key_press_callback(self._key_pressed)

        with window('Signals'):
            with tab_bar('tab_bar'):
                with tab('Plot'):
                    ui_add_plot()
                with tab('Signal Editor'):
                    ui_add_node_editor(self._link_added)

    def _key_pressed(self, sender, data):
        pass

    def start(self):
        start_dearpygui(primary_window='Signals')
        self._stopped()
