from PyQt5.QtCore import QTimer
from numpy import linspace, empty, pi, sin
from numpy.random import rand
from data_source_plugin import DataSourcePlugin

class DemoScopePlugin(DataSourcePlugin):
    scheme = 'demo'
    
    def __init__(self, parent):
        super().__init__(parent)
        self._timer = QTimer(parent)
        self._timer.timeout.connect(self._refresh)

        self._t = linspace(0, 1, 1000)
        self._y = empty(1000)

    def _refresh(self):
        self._y = sin(2*pi*10*self._t) + 0.1*rand(1000)
        self.y_changed.emit(self._y)

    def start(self):
        self._timer.start(100)
        self.t_changed.emit(self._t)
        self.y_changed.emit(self._y)

    def stop(self):
        self._timer.cancel()
