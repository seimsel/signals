from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from numpy import ndarray

class DataSourcePlugin(QObject):
    n_changed = pyqtSignal(int)
    t_changed = pyqtSignal(ndarray)
    y_changed = pyqtSignal(ndarray)
    scheme = None

    def __init__(self, parent):
        super().__init__(parent)

        if self.scheme == None:
            raise NotImplementedError('A DataSourcePlugin must define a scheme')

    def start(self):
        raise NotImplementedError('A DataSourcePlugin must implement a start method')

    def stop(self):
        raise NotImplementedError('A DataSourcePlugin must implement a stop method')
