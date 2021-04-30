from signals.parameters.path_parameter import PathParameter
from dearpygui.core import *
from dearpygui.simple import *

class SignalsUI:
    def __init__(self, signals):
        self._signals = signals

        with window('Signals'):
            with node_editor('Signal Editor'):
                pass
            
            with popup('Signal Editor', 'Signal Editor Context Menu'):
                pass

        set_key_press_callback(self._key_pressed)

    def _key_pressed(self, sender, data):
        if data == 259:
            for signal_name in get_selected_nodes('Signal Editor'):
                self._signals.remove_signal(signal_name)

    def signal_type_registered(self, signal_type):
        try:
            with menu(signal_type.category, parent='Signal Editor Context Menu'):
                pass
        except:
            pass

        def menu_item_clicked():
            self._signals.add_signal(signal_type())

        add_menu_item(signal_type.type_name, parent=signal_type.category, callback=menu_item_clicked)

    def signal_added(self, signal):
        signal.subscribe('parameter_changed', self.parameter_changed)

        with node(signal.name, parent='Signal Editor'):
            for parameter in signal.parameters:

                with node_attribute(f'{signal.name}_{parameter.name}_Attribute', static=True):
                    if type(parameter) == PathParameter:
                        def file_chosen(sender, data):
                            def callback(sender, data):
                                parameter.value = '/'.join(data)

                            open_file_dialog(callback=callback)

                        add_button(f'{signal.name}_{parameter.name}', callback=file_chosen, label=parameter.name)

    def parameter_changed(self, parameter):
        if type(parameter) == PathParameter:
            configure_item(f'{parameter.signal.name}_{parameter.name}', label=parameter.value.name)

    def signal_removed(self, signal):
        delete_item(signal.name)

    def start(self):
        start_dearpygui(primary_window='Signals')
