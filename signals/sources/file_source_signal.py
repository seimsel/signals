from ..source_signal import SourceSignal
from .. import PathParameter

class FileSourceSignal(SourceSignal):
    type_name = 'File'

    def __init__(self):
        super().__init__()
        self.add_parameter(PathParameter('Path'))
