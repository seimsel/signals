import sys

from numpy import linspace, sin, pi

import PyQt5.Qt as Qt
from PyQt5.QtGui import QGuiApplication, QColor
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGFlatColorMaterial

class Signal(QQuickItem):
    def __init__(self, parent):
        super().__init__(parent)
        self.n = int(1e3)

        self.x_range = [0, 1]
        self.y_range = [-1, 1]

        self.x = linspace(0, 1, self.n)
        self.y = sin(2*pi*10*self.x)

        self.setFlag(QQuickItem.ItemHasContents, True)
        self.geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(), self.n)
        self.geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
        self.geometry.setLineWidth(2)
        self.material = QSGFlatColorMaterial()
        self.material.setColor(QColor(255, 0, 0))

    def updatePaintNode(self, oldNode, updatePaintNodeData):
        node = oldNode

        if not node:
            node = QSGGeometryNode()
            node.setGeometry(self.geometry)
            node.setMaterial(self.material)

        points = self.geometry.vertexDataAsPoint2D()

        for i, point in enumerate(points):
            point.set(
                self.width()*self.x[i]/(self.x_range[1] - self.x_range[0]),
                self.height()/2 - self.height()*self.y[i]/(self.y_range[1] - self.y_range[0]))

        return node

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    qmlRegisterType(Signal, 'Signals', 0, 1, 'Signal')

    engine = QQmlApplicationEngine('signals.qml')
    exit(app.exec())
