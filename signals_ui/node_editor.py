from dearpygui.simple import (
    node_editor,
    node
)

def add_node_editor():
    with node_editor('node_editor'):
        pass

def add_node(id, name):
    with node(f'{name}##{id}', parent='node_editor'):        
        pass
