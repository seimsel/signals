import struct
import numpy
from enum import Enum
from vxi11 import Instrument

class LeCroyCommType(Enum):
    BYTE = 0
    WORD = 1

class LeCroyCommOrder(Enum):
    HIFIRST = 0
    LOFIRST = 1

class LeCroyWaveDesc:
    DESC_START = 0
    DESC_END = 346
    DESC_FORMAT = ''.join([
        '8s8x', # descriptor_name
        '16s',  # template_name,
        'H',    # comm_type
        'H',    # comm_order
        'L',    # wave_descriptor (length)
        'L',    # user_text (length)
        '4x',   # res_desc1 (length)
        'L',    # trigtime_array (length)
        'L',    # ris_time_array (length)
        '4x',   # res_array2 (length)
        'L',    # wave_array_1 (length)
        'L',    # wave_array_2 (length)
        '4x',   # res_array2 (length)
        '4x',   # res_array3 (length)
        '16s',  # instrument_name
        'L  ',  # instrument_number
        '16s',  # trace_label,
        '2x',   # reserved1
        '2x',   # reserved1
        'L'     # wave_array_count
    ])

    def __init__(self, data):
        rest_length = self.DESC_END - self.DESC_START - struct.calcsize(self.DESC_FORMAT)
        fmt = self.DESC_FORMAT + f'{rest_length}x'

        descriptor_items = struct.unpack(fmt, data)

        self.descriptor_name = descriptor_items[0].decode('ascii')
        self.template_name = descriptor_items[1].decode('ascii')
        self.comm_type = LeCroyCommType(descriptor_items[2])
        self.comm_order = LeCroyCommOrder(descriptor_items[3])
        self.wave_descriptor = int(descriptor_items[4])
        self.user_text = int(descriptor_items[5])
        self.trigtime_array = int(descriptor_items[6])
        self.ris_time_array = int(descriptor_items[7])
        self.wave_array_1 = int(descriptor_items[8])
        self.wave_array_2 = int(descriptor_items[9])
        self.instrument_name = descriptor_items[10].decode('ascii')
        self.instrument_number = int(descriptor_items[11])
        self.trace_label = descriptor_items[12].decode('ascii')
        self.wave_array_count = int(descriptor_items[13])

class LeCroyScope(Instrument):
    def __init__(self, address):
        super().__init__(address)
        self.write('COMM_ORDER LO')
        self.write('COMM_FORMAT OFF,BYTE,BIN')

    def read(self):
        self.write('C1:WAVEFORM? ALL')
        data_with_header = self.read_raw()
        data_offset = data_with_header.find(b'WAVEDESC')
        data = data_with_header[data_offset:-1]

        wave_desc = LeCroyWaveDesc(data[LeCroyWaveDesc.DESC_START:LeCroyWaveDesc.DESC_END])

        wave_array_1 = numpy.frombuffer(
            data[LeCroyWaveDesc.DESC_END+1:LeCroyWaveDesc.DESC_END+wave_desc.wave_array_1-1],
            dtype=numpy.int8
        )

        return wave_desc, wave_array_1
