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
        property double xPosition: 0.0
        property double yPosition: 0.0

        anchors.fill: parent

        onWheel: {
            if (wheel.modifiers & Qt.ControlModifier) {
                xScale += wheel.angleDelta.y/1200
                yScale += wheel.angleDelta.y/1200
                xOrigin = wheel.x
                yOrigin = wheel.y
                return;
            }

            xPosition += wheel.angleDelta.x
            yPosition += wheel.angleDelta.y
        }

        PinchArea {
            anchors.fill: parent

            property double xScale: 1.0
            property double yScale: 1.0

            onPinchStarted: {
                xScale = mouseArea.xScale
                yScale = mouseArea.yScale
            }
            
            onPinchUpdated: {
                mouseArea.xScale = xScale * pinch.scale
                mouseArea.yScale = yScale * pinch.scale
                mouseArea.xOrigin = pinch.center.x
                mouseArea.yOrigin = pinch.center.y
            }

            Signal {
                id: renderer
                anchors.fill: parent

                transform: [
                    Scale { xScale: renderer.width; yScale: renderer.height/2 },
                    Translate { y: renderer.height/2 },
                    Scale { origin.x: mouseArea.xOrigin; origin.y: mouseArea.yOrigin; xScale: mouseArea.xScale; yScale: mouseArea.yScale },
                    Translate { x: mouseArea.xPosition; y: mouseArea.yPosition }
                ]
            }
        }
    }
}
