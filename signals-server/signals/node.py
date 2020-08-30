from .api_object import ApiObject

class Node(ApiObject):
    def __init__(self):
        super().__init__()

        self.parent = None
        self._children = []

    @property
    def children(self):
        return self._children

    @property
    def childCount(self):
        return len(self._children)

    def appendChild(self, node):
        node.parent = self
        self._children.append(node)
