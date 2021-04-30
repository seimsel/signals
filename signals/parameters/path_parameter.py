from ..parameter import Parameter
from pathlib import Path

class PathParameter(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Parameter.value.setter
    def value(self, value):
        Parameter.value.fset(self, Path(value))
