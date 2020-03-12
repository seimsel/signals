from enum import Enum
from numpy import convolve, ones, zeros, concatenate, array
from parameters import FloatParameter, SourceParameter, SelectParameter
from channel import Channel

class _States(Enum):
    BOTTOM = 0
    RISING_EDGE_DETECTED = 1
    RISING = 2
    TOP = 3
    FALLING_EDGE_DETECTED = 4
    FALLING = 5

def get_edges(signal, level, hysteresis):
    lower_level = level - hysteresis
    higher_level = level + hysteresis

    rising_edges = []
    falling_edges = []
    current_state = _States.BOTTOM
    next_state = _States.BOTTOM

    for index, sample in enumerate(signal):
        if current_state == _States.BOTTOM:
            if sample > lower_level:
                next_state = _States.RISING_EDGE_DETECTED
            else:
                next_state = _States.BOTTOM
        elif current_state == _States.RISING_EDGE_DETECTED:
            rising_edges.append(index)
            next_state = _States.RISING
        elif current_state == _States.RISING:
            if sample > higher_level:
                next_state = _States.TOP
            else:
                next_state = _States.RISING
        elif current_state == _States.TOP:
            if sample < higher_level:
                next_state = _States.FALLING_EDGE_DETECTED
            else:
                next_state = _States.TOP
        elif current_state == _States.FALLING_EDGE_DETECTED:
            falling_edges.append(index)
            next_state = _States.FALLING
        elif current_state == _States.FALLING:
            if sample < lower_level:
                next_state = _States.BOTTOM
            else:
                next_state = _States.FALLING
        else:
            next_state = _States.BOTTOM

        current_state = next_state

    return rising_edges, falling_edges

def get_logic(signal, edges, level):
    data = []
    for i in edges:
        data.append(signal[i] > level)

    return array(data)

class DigitizeChannel(Channel):
    def __init__(self):
        super().__init__()
        
        self.clock = SourceParameter('Clock', self)
        self.signal = SourceParameter('Signal', self)
        self.edge = SelectParameter('Edge', 'rising', [
            'rising',
            'falling',
            'both'
        ])
        self.level = FloatParameter('Level', 0.5)
        self.hysteresis = FloatParameter('Hysteresis', 0.5)
        
        self.parameters = [
            self.clock,
            self.signal,
            self.edge,
            self.level,
            self.hysteresis
        ]

    @property
    def y(self):
        clock = self.scope.get_channel_by_name(self.clock.value)
        signal = self.scope.get_channel_by_name(self.signal.value)
        t_clock, y_clock = clock.data
        t_signal, y_signal = signal.data

        rising_edges, falling_edges = get_edges(
            y_clock,
            self.level.value,
            self.hysteresis.value)

        if self.edge.value == 'rising':
            edges = rising_edges
        elif self.edge.value == 'falling':
            edges = falling_edges
        elif self.edge.value == 'both':
            edges = rising_edges + falling_edges

        y_result = get_logic(
            y_signal,
            edges,
            self.level.value)

        self.start_time = clock.start_time
        self.end_time = clock.end_time
        self.sample_depth = len(y_result)

        return y_result

