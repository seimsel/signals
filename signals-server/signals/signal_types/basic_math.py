from numpy import copy
from ..signal import Signal

class AdditionSignal(Signal):
    name = 'Addition'
    category = 'Basic Math'

    def __init__(self, children, name):
        t = children[0].t
        y = copy(children[0].y)

        for child in children[1:]:
            y += child.y

        super().__init__(t, y, name)
        self.add_children(children)

class SubstractionSignal(Signal):
    name = 'Substraction'
    category = 'Basic Math'

    def __init__(self, children, name):
        t = children[0].t
        y = copy(children[0].y)

        for child in children[1:]:
            y -= child.y

        super().__init__(t, y, name)
        self.add_children(children)

class MultiplicationSignal(Signal):
    name = 'Multiplication'
    category = 'Basic Math'

    def __init__(self, children, name):
        t = children[0].t
        y = copy(children[0].y)

        for child in children[1:]:
            y *= child.y

        super().__init__(t, y, name)
        self.add_children(children)

class DivisionSignal(Signal):
    name = 'Division'
    category = 'Basic Math'

    def __init__(self, children, name):
        t = children[0].t
        y = children[0].y

        for child in children[1:]:
            y /= child.y

        super().__init__(t, y, name)
        self.add_children(children)
