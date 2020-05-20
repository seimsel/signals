from sys import argv

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from matplotlib_backend_qtquick.backend_qtquickagg import FigureCanvasQtQuickAgg

class Test(QObject):

    @pyqtSlot(FigureCanvasQtQuickAgg)
    def func(self, canvas):
        axis = canvas.figure.add_subplot('111')
        axis.plot([1, 2, 3])
        canvas.draw()

if __name__ == "__main__":
    app = QGuiApplication(argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType(FigureCanvasQtQuickAgg, 'Matplotlib', 0, 1, 'FigureCanvas')

    test = Test()

    context = engine.rootContext()
    context.setContextProperty('test', test)

    engine.load('signals.qml')

    exit(app.exec())
