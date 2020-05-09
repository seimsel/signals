from data_source_plugin import DataSourcePlugin
from threading import Timer

class DemoScopePlugin(DataSourcePlugin):
    scheme = 'demo'
    
    def __init__(self, parent):
        super().__init__(parent)
        self._timer = Timer(1, self.refresh)

    def refresh(self):
        print('refresh')
        self.t_changed.emit()
        self.y_changed.emit()

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()
