from PyQt5.QtCore import QTimer
from numpy import linspace, empty, pi, sin
from numpy.random import default_rng
from data_source_plugin import DataSourcePlugin

class DemoScopePlugin(DataSourcePlugin):
    scheme = 'demo'
    
    def __init__(self, parent):
        super().__init__(parent)
        self._timer = QTimer(parent)
        self._timer.timeout.connect(self._refresh)

        self._noise_generator = default_rng()

        self._n = 10000
        self._t = linspace(0, 1, self._n)
        self._y = empty(len(self._t))

    def _refresh(self):
        self._y = sin(2*pi*10*self._t) + self._noise_generator.normal(0.0, 0.1, len(self._t))
        self.y_changed.emit(self._y)

    def start(self):
        self._timer.start(10)
        self.n_changed.emit(self._n)
        self.t_changed.emit(self._t)
        self.y_changed.emit(self._y)

    def stop(self):
        self._timer.cancel()
