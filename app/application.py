from PyQt5.QtWidgets import QApplication

import ctypes
import platform
import struct

class Application(QApplication):
    def __init__(self):
        super().__init__([])

    def start(self):
        self.exec_()
