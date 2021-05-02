from ..source_signal import SourceSignal

import numpy as np

class FileSourceSignal(SourceSignal):
    type_name = 'File'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_changed = True

    async def process(self):
        while not self.file_changed:
            pass

        self.file_changed = False
        results = np.loadtxt('example.csv').T[1:]
        self.output_descriptor = len(results)
        return results
