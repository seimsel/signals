from dearpygui.simple import window
from ..source_signal import SourceSignal

import numpy as np

class FileSourceSignal(SourceSignal):
    type_name = 'File'

    def __init__(self):
        super().__init__()
        self.file_changed = True

    async def process(self):
        while not self.file_changed:
            pass

        self.file_changed = False
        return np.loadtxt('example.csv').T[1:]
