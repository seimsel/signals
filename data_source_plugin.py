from PyQt5.QtCore import QObject, pyqtSignal, QUrl

class DataSourcePlugin(QObject):
    t_changed = pyqtSignal()
    y_changed = pyqtSignal()
    scheme = None

    def __init__(self, parent):
        super().__init__(parent)

        if self.scheme == None:
            raise NotImplementedError('A DataSourcePlugin must define a scheme')

    def start(self):
        raise NotImplementedError('A DataSourcePlugin must implement a start method')

    def stop(self):
        raise NotImplementedError('A DataSourcePlugin must implement a stop method')
