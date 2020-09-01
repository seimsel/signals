from .api_object import ApiObject

class Node(ApiObject):
    def __init__(self, isRoot=False):
        super().__init__()

        self.isRoot = isRoot
        self.root = None
        self.parent = None
        self._children = []

        if self.isRoot:
            self.nodes = {}

    @property
    def children(self):
        return self._children

    @property
    def childCount(self):
        return len(self._children)

    def appendChild(self, node):
        node.parent = self

        if self.isRoot:
            self.nodes[node.id] = node
            node.root = self

        self._children.append(node)
