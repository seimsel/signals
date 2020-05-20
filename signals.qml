import QtQuick.Window 2.2
import QtQuick 2.14
import Matplotlib 0.1

Window {
    visible: true

    width: 800
    height: 600

    FigureCanvas {
        id: canvas
        anchors.fill: parent

        Component.onCompleted: {
            test.func(canvas)
        }
    }
}
