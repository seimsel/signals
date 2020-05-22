from sys import argv

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication, QWidget, QFileDialog

from numpy import genfromtxt
from matplotlib import use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SignalsWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()
        self.view = view

        fileMenu = self.menuBar().addMenu('&File')
        openAction = fileMenu.addAction('&Open...')
        openAction.triggered.connect(self.open)

        self.figure = Figure()
        self.axis = self.figure.add_subplot('111')

        self.figureCanvas = FigureCanvas(self.figure)

        self.setCentralWidget(self.figureCanvas)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)

        data = genfromtxt(fileName, delimiter=',').T
        self.axis.plot(data[0], *data[1:])
        self.figureCanvas.draw()

class SignalsView(QWidget):
    def __init__(self):
        super().__init__()

        self.windows = [
            SignalsWindow(self)
        ]

    def show(self):
        for window in self.windows:
            window.show()

def main():
    use('Qt5Agg')

    app = QApplication(argv)
    view = SignalsView()

    view.show()

    exit(app.exec())


if __name__ == '__main__':
    main()