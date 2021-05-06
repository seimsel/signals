from dearpygui.core import (
    add_menu_item,
    add_node_link,
    add_text,
    get_links
)

from dearpygui.simple import (
    node_attribute,
    node_editor,
    node,
    menu,
    popup
)

class NodeAttribute:
    def __init__(self, name, type='input'):
        self.name = name
        self.type = type

def ui_add_node_editor(link_added):
    def link_callback():
        new_link = get_links('node_editor')[-1]
        source_attribute_name, source_id = new_link[0].split('##')
        sink_attribute_name, sink_id = new_link[1].split('##')
        link_added(source_id, source_attribute_name, sink_id, sink_attribute_name)

    with node_editor('node_editor', link_callback=link_callback):
        pass

    with popup('node_editor', 'node_editor_context_menu', mousebutton=1):
        pass

def ui_add_node_type(category, type, on_add_node):
    try:
        with menu(category, parent='node_editor_context_menu'):
            pass
    except:
        pass

    add_menu_item(f'{type}##{category}', parent=category, callback=lambda: on_add_node())

def ui_add_node(id, name, attributes):
    with node(f'{name}##{id}', parent='node_editor'):       
        for attribute in attributes:
            is_output = True if attribute.type == 'output' else False
            
            with node_attribute(f'{attribute.name}##{id}', output=is_output):
                add_text(f'{attribute.name}')

def ui_add_node_link(source_id, source_attribute_name, sink_id, sink_attribute_name):
    if [
        f'{source_attribute_name}##{source_id}',
        f'{sink_attribute_name}##{sink_id}'
    ] in get_links('node_editor'):
        return

    add_node_link(
        'node_editor',
        f'{source_attribute_name}##{source_id}',
        f'{sink_attribute_name}##{sink_id}'
    )
