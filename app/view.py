from .browser_window import BrowserWindow
from PyQt5.QtCore import QObject

class View(QObject):
    def __init__(self):
        super().__init__()

        self.windows = [
            BrowserWindow()
        ]

        for window in self.windows:
            window.show()
