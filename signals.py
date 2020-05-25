from sys import argv

from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QUrl, QAbstractItemModel, QModelIndex
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMainWindow, QAction, QMenu, QDockWidget, QApplication, QWidget, QFileDialog

from numpy import genfromtxt
from matplotlib import use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class SignalsToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom')]

class Signal():
    def __init__(self, t, y, name):
        self.t = t
        self.y = y
        self.name = name

class Measurement():
    pass

class FileMeasurement(Measurement):
    scheme = 'file://'

    def __init__(self, url):
        self.url = url
        data = genfromtxt(self.url.toLocalFile(), delimiter=',').T

        self.signals = []

        t = data[0]

        for i, y in enumerate(data[1:]):
            self.signals.append(Signal(t, y, f'Signal {i}'))

class SignalsApplication(QApplication):
    def __init__(self):
        super().__init__(argv)

        initialWindow = SignalsWindow(self)
        initialWindow.measurement = None

        self.windows = [
            initialWindow
        ]

        initialWindow.show()

    def open(self, window, fileName):
        url = QUrl.fromLocalFile(fileName)
        
        for window in self.windows:
            # If the file is already open, focus the window
            if type(window.measurement) == FileMeasurement and window.measurement.url == url:
                window.activateWindow()
                break
        else:
            # If the window is empty, use this window...
            if not window.measurement:
                window.measurement = FileMeasurement(url)
            # else create a new window
            else:
                newWindow = SignalsWindow(self)
                newWindow.measurement = FileMeasurement(url)
                newWindow.show()
                self.windows.append(newWindow)

class SignalsWindow(QMainWindow):
    measurementChanged = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app

        fileMenu = self.menuBar().addMenu('&File')
        openAction = fileMenu.addAction('&Open...')
        openAction.triggered.connect(self.open)

        self.figure = Figure()
        self.axis = self.figure.add_subplot('111')

        self.figureCanvas = FigureCanvas(self.figure)

        toolBar = SignalsToolbar(self.figureCanvas, self)
        self.addToolBar(toolBar)

        self.setCentralWidget(self.figureCanvas)

        self.treeView = QTreeWidget()
        dockWidget = QDockWidget('Signals')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dockWidget)
        dockWidget.setWidget(self.treeView)

        self.measurementChanged.connect(self.onMeasurementChanged)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        self.app.open(self, fileName)
    
    @pyqtProperty(Measurement, notify=measurementChanged)
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, measurement):
        self._measurement = measurement
        self.measurementChanged.emit()

    def onMeasurementChanged(self):
        if not self.measurement:
            return

        root = QTreeWidgetItem([self.measurement.url.fileName()])

        for signal in self.measurement.signals:
            self.axis.plot(signal.t, signal.y)
            root.addChild(QTreeWidgetItem([signal.name]))

        self.treeView.addTopLevelItem(root)

        self.figureCanvas.draw()

def main():
    use('Qt5Agg')
    app = SignalsApplication()
    exit(app.exec())


if __name__ == '__main__':
    main()