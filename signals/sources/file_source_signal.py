from ..source_signal import SourceSignal
import numpy as np
from pathlib import Path

class FileSourceSignal(SourceSignal):
    type_name = 'File'

    def __init__(self, name, path=None):
        if path:
            path = Path(path)

        super().__init__(name, path=path)

    def process(self):
        return np.loadtxt(self.path).T
