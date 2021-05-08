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
        input_data = np.loadtxt(str(self.path)).T
        output_data = {
            't': input_data[0]
        }
        
        for i, channel in enumerate(input_data[1:]):
            output_data[f'Ch_{i+1}'] = channel

        return output_data
