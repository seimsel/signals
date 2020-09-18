from .browser_window import BrowserWindow
from PyQt5.QtCore import QObject

class View(QObject):
    def __init__(self, ui_http_url, development):
        super().__init__()

        self.windows = [
            BrowserWindow(ui_http_url, development)
        ]

        for window in self.windows:
            window.show()
