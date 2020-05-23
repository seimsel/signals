from sys import argv

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication, QWidget, QFileDialog

from numpy import genfromtxt
from matplotlib import use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Model(QObject):
    pass

class EmptyModel(Model):
    pass

class CSVModel(Model):
    def __init__(self, fileName):
        super().__init__()
        self.fileName = fileName
        self.data = genfromtxt(fileName, delimiter=',').T

class SignalsApplication(QApplication):
    def __init__(self):
        super().__init__(argv)

        initialWindow = SignalsWindow(self)
        initialWindow.model = EmptyModel()

        self.windows = [
            initialWindow
        ]

        initialWindow.show()

    def open(self, window, fileName):
        for window in self.windows:
            # If the file is already open, focus the window
            if type(window.model) == CSVModel and window.model.fileName == fileName:
                window.activateWindow()
                break
        else:
            # If the window is empty, use this window...
            if type(window.model) == EmptyModel:
                window.model = CSVModel(fileName)
            # else create a new window
            else:
                newWindow = SignalsWindow(self)
                newWindow.model = CSVModel(fileName)
                newWindow.show()
                self.windows.append(newWindow)

class SignalsWindow(QMainWindow):
    modelChanged = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app

        fileMenu = self.menuBar().addMenu('&File')
        openAction = fileMenu.addAction('&Open...')
        openAction.triggered.connect(self.open)

        self.figure = Figure()
        self.axis = self.figure.add_subplot('111')

        self.figureCanvas = FigureCanvas(self.figure)

        self.setCentralWidget(self.figureCanvas)
        self.modelChanged.connect(self.onModelChanged)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        self.app.open(self, fileName)
    
    @pyqtProperty(Model, notify=modelChanged)
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
        self.modelChanged.emit()

    def onModelChanged(self):
        if type(self.model) == EmptyModel:
            return

        self.axis.plot(self.model.data[0], *self.model.data[1:])
        self.figureCanvas.draw()

def main():
    use('Qt5Agg')
    app = SignalsApplication()
    exit(app.exec())


if __name__ == '__main__':
    main()