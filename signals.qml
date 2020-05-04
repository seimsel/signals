import QtQuick.Window 2.2
import QtQuick 2.14
import Signals 0.1

Window {
    visible: true

    MouseArea {
        id: mouseArea

        property double xScale: 1.0
        property double yScale: 1.0
        property double xOrigin: parent.width/2
        property double yOrigin: parent.height/2

        anchors.fill: parent
        onWheel: {
            xScale += wheel.angleDelta.y/1200
            yScale += wheel.angleDelta.y/1200
            xOrigin = wheel.x
            yOrigin = wheel.y
        }

        Signal {
            id: renderer
            anchors.fill: parent

            transform: [
                Scale { xScale: renderer.width; yScale: renderer.height/2 },
                Translate { y: renderer.height/2 },
                Scale { origin.x: mouseArea.xOrigin; origin.y: mouseArea.yOrigin; xScale: mouseArea.xScale; yScale: mouseArea.yScale }
            ]
        }
    }
}
