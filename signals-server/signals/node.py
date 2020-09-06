from .api_object import ApiObject
from ariadne import InterfaceType

from functools import reduce

node_type = InterfaceType('Node')

@node_type.type_resolver
def resolve_node_type(obj, *_):
    return type(obj).__name__

class Node(ApiObject):
    def __init__(self, isRoot=False):
        super().__init__()

        self.null = None
        self.isRoot = isRoot
        self._root = None
        self.parents = []
        self._children = []

        if self.isRoot:
            self.nodes = {}

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node):
        self._root = node

        count = len(list(filter(lambda obj: type(obj) == type(self), self.root.nodes.values())))
        self.name = f'{type(self).__name__} {count + 1}'

    def is_type_of():
        return type(self)

    @property
    def children(self):
        return self._children

    @property
    def childCount(self):
        return len(self._children)

    def appendChild(self, node):
        node.parents.append(self)

        if self.isRoot:
            node.root = self
        else:
            node.root = node.parents[0].root

        node.root.nodes[node.id] = node

        self._children.append(node)
