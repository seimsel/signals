from sys import argv

from PyQt5.QtCore import QObject, QUrl, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

from numpy import genfromtxt

class Controller(QObject):

    @pyqtSlot(QUrl)
    def open(self, url):
        data = genfromtxt(url.toLocalFile(), delimiter=',')
        axis = self.canvas.figure.add_subplot('111')
        axis.plot(data[0], *data[1:])
        self.canvas.draw()

    @pyqtSlot(FigureCanvasQtQuickAgg)
    def setCanvas(self, canvas):
        self.canvas = canvas

if __name__ == "__main__":
    app = QGuiApplication(argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(FigureCanvasQtQuickAgg, 'Matplotlib', 0, 1, 'FigureCanvas')

    controller = Controller()

    context = engine.rootContext()
    context.setContextProperty('controller', controller)

    engine.load('signals.qml')

    exit(app.exec())
