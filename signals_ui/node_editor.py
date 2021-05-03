from dearpygui.core import add_node_link, add_text
from dearpygui.simple import (
    node_attribute,
    node_editor,
    node
)

class NodeAttribute:
    def __init__(self, name, type='input'):
        self.name = name
        self.type = type

def ui_add_node_editor():
    with node_editor('node_editor'):
        pass

def ui_add_node(id, name, attributes):
    with node(f'{name}##{id}', parent='node_editor'):       
        for attribute in attributes:
            is_output = True if attribute.type == 'output' else False
            
            with node_attribute(f'{attribute.name}##{id}', output=is_output):
                add_text(f'{attribute.name}')

def ui_add_node_link(source_id, source_attribute_name, sink_id, sink_attribute_name):
    print(source_id)
    print(source_attribute_name)
    print(sink_id)
    print(sink_attribute_name)

    add_node_link(
        'node_editor',
        f'{source_attribute_name}##{source_id}',
        f'{sink_attribute_name}##{sink_id}'
    )
