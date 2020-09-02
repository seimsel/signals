from .api_object import ApiObject
from ariadne import InterfaceType

node_type = InterfaceType('Node')

@node_type.type_resolver
def resolve_node_type(obj, *_):
    return type(obj).__name__

class Node(ApiObject):
    def __init__(self, isRoot=False):
        super().__init__()

        self.null = None
        self.isRoot = isRoot
        self.root = None
        self.parent = None
        self._children = []

        if self.isRoot:
            self.nodes = {}
            self.nodes[self.id] = self

    def is_type_of():
        return type(self)

    @property
    def children(self):
        return self._children

    @property
    def childCount(self):
        return len(self._children)

    def appendChild(self, node):
        node.parent = self

        if self.isRoot:
            node.root = self
        else:
            node.root = node.parent.root

        node.root.nodes[node.id] = node

        self._children.append(node)
