from dearpygui.core import *
from dearpygui.simple import *

def update_nodes(signals):
    items = get_all_items()
    for signal in signals.values():
        if f'signal_{signal.id}' in items:
            continue

        with node(f'signal_{signal.id}', parent='Node_Editor', label=signal.name):
            inputs = signal.input_descriptor
            
            if type(inputs) == int:
                inputs = range(0, inputs)
            
            for input in inputs:
                with node_attribute(f'input_{signal.id}_I_{input}'):
                    add_text(f'I_{input}')

            outputs = signal.output_descriptor
            
            if type(outputs) == int:
                outputs = range(0, outputs)

            for output in outputs:
                with node_attribute(f'output_{signal.id}_O_{output}', output=True):
                    add_text(f'O_{output}')

    for item in items:
        if 'signal_' in item and f'{item[7:]}' not in signals.keys():
            delete_item(item)

def remove_selected_nodes(callback):
    for node_id in get_selected_nodes('Node_Editor'):
        callback(node_id[7:])

def update_links(connections):
    for connection in connections.values():
            add_node_link(
                'Node_Editor',
                f'output_{connection.source_id}_O_{connection.output}',
                f'input_{connection.sink_id}_I_{connection.input}'
            )
