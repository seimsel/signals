import sys

from numpy import linspace, sin, pi, float16

import PyQt5.Qt as Qt
from PyQt5.QtCore import pyqtProperty, QUrl
from PyQt5.QtGui import QGuiApplication, QColor
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickItem, QSGNode, QSGGeometryNode, QSGGeometry, QSGFlatColorMaterial

from plugins.demo_scope_plugin import DemoScopePlugin

class Signal(QQuickItem):
    def __init__(self, parent):
        super().__init__(parent)

        self._source = None

        self.data_source_plugins = [
            DemoScopePlugin(self)
        ]

        self.n = int(1e3)

        self.x_range = [0, 1]
        self.y_range = [-1, 1]

        self.t = None
        self.y = None

        self.dirty = True

        self.setFlag(QQuickItem.ItemHasContents, True)
        self.geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(), self.n)
        self.geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
        self.geometry.setLineWidth(2)
        self.material = QSGFlatColorMaterial()
        self.material.setColor(QColor(0, 0, 0))

    @pyqtProperty(QUrl)
    def source(self):
        return self._source

    @source.setter
    def source(self, url):
        for plugin in self.data_source_plugins:
            if url.scheme() == plugin.scheme:
                plugin.t_changed.connect(self.onTChanged)
                plugin.y_changed.connect(self.onYChanged)
                plugin.start()
            else:
                plugin.stop()
                plugin.t_changed.disconnect(self.onTChanged)
                plugin.y_changed.disconnect(self.onYChanged)

        self._source = url

    def onTChanged(self, t):
        self.x = t
        self.dirty = True
        self.update()

    def onYChanged(self, y):
        self.y = y
        self.dirty = True
        self.update()

    def updatePaintNode(self, oldNode, updatePaintNodeData):
        node = oldNode

        if node == None or self.dirty:
            if node == None:
                node = QSGGeometryNode()
                node.setGeometry(self.geometry)
                node.setMaterial(self.material)

            points = self.geometry.vertexDataAsPoint2D()

            for i, point in enumerate(points):
                point.set(self.x[i], -self.y[i])

            node.markDirty(QSGNode.DirtyGeometry)

            self.dirty = False

        return node        

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    qmlRegisterType(Signal, 'Signals', 0, 1, 'Signal')
    engine = QQmlApplicationEngine('signals.qml')
    exit(app.exec())
