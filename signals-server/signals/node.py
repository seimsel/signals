from ariadne import InterfaceType
from .api_object import ApiObject

node_type = InterfaceType('Node')

@node_type.type_resolver
def resolve_node_type(obj, *_):
    return obj.type

class Node(ApiObject):
    def __init__(self):
        super().__init__()
        self._children = []

    @property
    def children(self):
        return self._children
    
    @property
    def child_count(self):
        return len(self._children)

    def add_child(self, child):
        self._children.append(child)

    def add_children(self, children):
        self._children.extend(children)

    @property
    def nodes(self):
        count = self.child_count

        items = []

        for child in self.children:
            items.append(child)
            items += child.nodes
        
        return items
