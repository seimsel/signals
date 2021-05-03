from dearpygui.core import add_text
from dearpygui.simple import (
    node_attribute,
    node_editor,
    node
)

class NodeAttribute:
    def __init__(self, name, type='input'):
        self.name = name
        self.type = type

def add_node_editor():
    with node_editor('node_editor'):
        pass

def add_node(id, name, attributes):
    with node(f'{name}##{id}', parent='node_editor'):       
        for attribute in attributes:
            is_output = True if attribute.type == 'output' else False
            
            with node_attribute(f'{attribute.name}##{id}', output=is_output):
                add_text(f'{attribute.name}')
