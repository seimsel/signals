import struct
import numpy as np
from enum import Enum
from scope import Scope
from channel import Channel
from channels.moving_average import MovingAverageChannel
from parameters import SelectParameter

try:
    import vxi11
except:
    print('vxi11 not installed or not available')

class LeCroyChannel(Channel):
    @property
    def y(self):
        if not self.scope.interface:
            self.scope.interface = vxi11.Instrument(self.scope.address)
            self.scope.interface.write('COMM_ORDER LO')
            self.scope.interface.write('COMM_FORMAT OFF,BYTE,BIN')

        self.scope.interface.write(f'{self.name}:WAVEFORM? ALL')
        data_with_header = self.scope.interface.read_raw()
        data_offset = data_with_header.find(b'WAVEDESC')
        data = data_with_header[data_offset:-1]

        wave_desc = LeCroyWaveDesc(data[LeCroyWaveDesc.DESC_START:LeCroyWaveDesc.DESC_END])

        y = np.frombuffer(
            data[LeCroyWaveDesc.DESC_END+1:LeCroyWaveDesc.DESC_END+wave_desc.wave_array_1-1],
            dtype=np.int8
        )

        self.start_time = 0
        self.end_time = 1
        self.sample_depth = len(y)

        return y

class C1(LeCroyChannel):
    pass

class C2(LeCroyChannel):
    pass

class C3(LeCroyChannel):
    pass

class C4(LeCroyChannel):
    pass

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
        '<',        # alignment
        '8s8x',     # descriptor_name
        '16s',      # template_name,
        'H',        # comm_type
        'H',        # comm_order
        'L',        # wave_descriptor (length)
        'L',        # user_text (length)
        '4x',       # res_desc1 (length)
        'L',        # trigtime_array (length)
        'L',        # ris_time_array (length)
        '4x',       # res_array2 (length)
        'L',        # wave_array_1 (length)
        'L',        # wave_array_2 (length)
        '4x',       # res_array2 (length)
        '4x',       # res_array3 (length)
        '16s',      # instrument_name
        'L  ',      # instrument_number
        '16s',      # trace_label,
        '2x',       # reserved1
        '2x',       # reserved2
        'L',        # wave_array_count
        'L',        # pnts_per_screen
        'L',        # first_valid_pnt
        'L',        # last_valid_pnt
        'L',        # first_point
        'L',        # sparsing_factor
        'L',        # segment_index
        'L',        # subarray_count
        'L',        # sweeps_per_acq
        'H',        # points_per_pair
        'H',        # pair_offset
        'f',        # vertical_gain
        'f',        # vertical_offset
        'f',        # max_value
        'f',        # min_value
        'H',        # nominal_bits
        'H',        # nom_subarray_count
        'f',        # horiz_interval
        'd',        # horiz_offset
        'd',        # pixel_offset
        '48s',      # vertunit
        '48s',      # horunit
        'f',        # horiz_uncertainty
        'dBBBBH2x', # trigger_time
        'f'         # acq_duration
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
        self.pnts_per_screen = int(descriptor_items[14])
        self.first_valid_pnt = int(descriptor_items[15])
        self.last_valid_pnt = int(descriptor_items[16])
        self.first_point = int(descriptor_items[17])
        self.sparsing_factor = int(descriptor_items[18])
        self.segment_index = int(descriptor_items[19])
        self.subarray_count = int(descriptor_items[20])
        self.sweeps_per_acq = int(descriptor_items[21])
        self.points_per_pair = int(descriptor_items[22])
        self.pair_offset = int(descriptor_items[23])
        self.vertical_gain = float(descriptor_items[24])
        self.vertical_offset = float(descriptor_items[25])
        self.max_value = float(descriptor_items[26])
        self.min_value = float(descriptor_items[27])
        self.nominal_bits = int(descriptor_items[28])
        self.nom_subarray_count = int(descriptor_items[29])
        self.horiz_interval = float(descriptor_items[30])
        self.horiz_offset = float(descriptor_items[31])
        self.pixel_offset = float(descriptor_items[32])
        self.vertunit = descriptor_items[33].decode('ascii')
        self.horunit = descriptor_items[34].decode('ascii')
        self.horiz_uncertainty = float(descriptor_items[35])
        self.trigger_time = str(descriptor_items[36:42])
        self.acq_duration = float(descriptor_items[42])

class LeCroyScope(Scope):
    def __init__(self, address):
        super().__init__(address)

        self.interface = None

        self.channel_types = [
            C1,
            C2,
            C3,
            C4,
            MovingAverageChannel
        ]
