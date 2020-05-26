from sys import argv
from pathlib import Path

from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QUrl, QAbstractItemModel, QModelIndex
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QMainWindow, QAction, QMenu, QDockWidget, QApplication, QWidget, QFileDialog

from numpy import genfromtxt
from matplotlib import use
from matplotlib.pyplot import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

style.use(str(Path(__file__).with_name('dark.mplstyle')))

class Signal(QTreeWidgetItem):
    def __init__(self, t, y, name):
        super().__init__([name])
        self.t = t
        self.y = y
        self.name = name

class AdditionSignal(Signal):
    name = 'Addition'
    category = 'Basic Math'

    def __init__(self, children, name):
        y = 0

        for child in children:
            y += child.y

        super().__init__(children[0].t, y, name)
        self.addChildren(children)

SignalTypes = [
    AdditionSignal
]

class SignalsToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom')]

class Measurement(QTreeWidgetItem):
    def __init__(self, url):
        super().__init__([url.fileName()])
        self.url = url

    def signals(self, item=None):
        if not item:
            item = self

        count = item.childCount()

        items = []

        for i in range(0, count):
            child = item.child(i)
            items.append(child)
            items += self.signals(child)

        return items

class FileMeasurement(Measurement):
    scheme = 'file://'

    def __init__(self, url):
        super().__init__(url)
        data = genfromtxt(self.url.toLocalFile(), delimiter=',').T

        t = data[0]

        for i, y in enumerate(data[1:]):
            self.addChild(Signal(t, y, f'Signal {i}'))

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

        editMenu = self.menuBar().addMenu('&Edit')
        addMenu = editMenu.addMenu('&Add')

        self.categoryMenus = {}

        for signalType in SignalTypes:
            category = signalType.category

            menu = self.categoryMenus.get(category, None)

            if not menu:
                menu = addMenu.addMenu(category)
                self.categoryMenus[category] = menu
            
            action = menu.addAction(signalType.name)
            action.triggered.connect(lambda: self.addSignal(signalType))

        self.figure = Figure()

        self.figureCanvas = FigureCanvas(self.figure)

        toolBar = SignalsToolbar(self.figureCanvas, self)
        self.addToolBar(toolBar)

        self.setCentralWidget(self.figureCanvas)

        self.treeView = QTreeWidget()
        self.treeView.setHeaderHidden(True)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        dockWidget = QDockWidget('Signals')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dockWidget)
        dockWidget.setWidget(self.treeView)

        self.measurementChanged.connect(self.onMeasurementChanged)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        self.app.open(self, fileName)

    def addSignal(self, signalType):
        selectedItems = self.treeView.selectedItems()

        root = selectedItems[0].parent()
        for item in selectedItems:
            parent = item.parent()
            parent.removeChild(item)

            if root != parent:
                root = self.measurement

        signal = signalType(selectedItems, 'Signal')
        root.addChild(signal)
        self.measurementChanged.emit()
    
    @pyqtProperty(Measurement, notify=measurementChanged)
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, measurement):
        self._measurement = measurement
        self.measurementChanged.emit()

    def onMeasurementChanged(self):
        self.figure.clear()
        
        if not self.measurement:
            return

        self.axis = self.figure.add_subplot('111')

        for signal in self.measurement.signals():
            self.axis.plot(signal.t, signal.y)

        self.treeView.addTopLevelItem(self.measurement)

        self.figureCanvas.draw()

def main():
    use('Qt5Agg')
    app = SignalsApplication()
    exit(app.exec())


if __name__ == '__main__':
    main()