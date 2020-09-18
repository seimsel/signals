from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QUrl

class Python(QObject):
    fileNamesChanged = pyqtSignal(list)

    @pyqtSlot()
    def getOpenFileNames(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self.parent())
        self.fileNamesChanged.emit(fileNames)

class BrowserWindow(QWebEngineView):
    def __init__(self, ui_http_url):
        super().__init__()
        channel = QWebChannel(self)
        channel.registerObject('python', Python(self))
        self.page().setWebChannel(channel)
        self.load(QUrl(ui_http_url))
