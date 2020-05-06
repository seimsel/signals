import QtQuick.Window 2.2
import QtQuick 2.14
import Signals 0.1

Window {
    visible: true

    width: 800
    height: 600

    MouseArea {
        id: mouseArea

        anchors.fill: parent

        onWheel: {
            if (wheel.modifiers & Qt.ControlModifier) {
                const previousXScale = zoom.xScale
                const previousYScale = zoom.yScale

                zoom.xScale += wheel.angleDelta.x/1200
                zoom.yScale += wheel.angleDelta.y/1200

                position.x -= (wheel.x - position.x)*(zoom.xScale/previousXScale) - (wheel.x - position.x)
                position.y -= (wheel.y - position.y)*(zoom.yScale/previousYScale) - (wheel.y - position.y)
                return;
            }

            position.x += wheel.angleDelta.x
            position.y += wheel.angleDelta.y
        }

        PinchArea {
            anchors.fill: parent

            property double storedXScale: 1.0
            property double storedYScale: 1.0

            property bool zoomX: false
            property bool zoomY: false

            MultiPointTouchArea {
                anchors.fill: parent
                maximumTouchPoints: 2
                minimumTouchPoints: 2

                onPressed: {
                    if (touchPoints.length === 2) {
                        const xyDifference = Math.abs(touchPoints[0].x - touchPoints[1].x) - Math.abs(touchPoints[0].y - touchPoints[1].y)

                        if (xyDifference > 50)  {
                            parent.zoomX = true
                            parent.zoomY = false
                        } else if (xyDifference < -50) {
                            parent.zoomX = false
                            parent.zoomY = true
                        } else {
                            parent.zoomX = true
                            parent.zoomY = true    
                        }
                    }
                }
            }

            onPinchStarted: {
                storedXScale = zoom.xScale
                storedYScale = zoom.yScale
            }
            
            onPinchUpdated: {
                const previousXScale = zoom.xScale
                const previousYScale = zoom.yScale

                if (zoomX) {
                    zoom.xScale = storedXScale * pinch.scale
                }
                
                if (zoomY) {
                    zoom.yScale = storedYScale * pinch.scale
                }

                position.x -= (pinch.center.x - position.x)*(zoom.xScale/previousXScale) - (pinch.center.x - position.x)
                position.y -= (pinch.center.y - position.y)*(zoom.yScale/previousYScale) - (pinch.center.y - position.y)

            }

            Signal {
                id: renderer
                anchors.fill: parent

                transform: [
                    Scale { xScale: renderer.width; yScale: renderer.height/2 },
                    Translate { y: renderer.height/2 },
                    Scale { id: zoom },
                    Translate { id: position }
                ]
            }
        }
    }
}
