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

        acceptedButtons: Qt.LeftButton | Qt.RightButton

        property bool panning: false
        property bool zooming: false

        property double storedXPosition: 0.0
        property double storedYPosition: 0.0
        property double previousXPosition: 0.0
        property double previousYPosition: 0.0

        Rectangle {
            id: selection

            border.color: 'black'
            border.width: 2

            visible: false
        }

        Keys.onEscapePressed: {
            zooming = false
        }

        onZoomingChanged: {
            selection.visible = zooming
            mouseArea.focus = zooming
        }

        onPressed: {
            if (
                mouse.button === Qt.LeftButton
                && mouse.modifiers & Qt.ControlModifier
            ) {
                previousXPosition = mouse.x
                previousYPosition = mouse.y
                panning = true
            } else if (mouse.button === Qt.LeftButton) {
                storedXPosition = mouse.x
                storedYPosition = mouse.y
                selection.width = 0
                selection.height = 0
                zooming = true
            } else if (mouse.button === Qt.RightButton) {
                position.x = 0.0
                position.y = 0.0
                zoom.xScale = 1.0
                zoom.yScale = 1.0
            }
        }

        onReleased: {
            if (mouse.button === Qt.LeftButton && zooming) {
                const previousXScale = zoom.xScale
                const previousYScale = zoom.yScale

                zooming = false

                if (selection.width < 10 || selection.height < 10) {
                    return;
                }

                zoom.xScale *= mouseArea.width/selection.width
                zoom.yScale *= mouseArea.height/selection.height

                position.x -= (mouse.x - selection.width/2 - position.x)*(zoom.xScale/previousXScale) - (mouse.x - selection.width/2 - position.x)
                position.y -= (mouse.y - selection.height/2 - position.y)*(zoom.yScale/previousYScale) - (mouse.y - selection.height/2 - position.y)
            }

            if (mouse.button === Qt.RightButton && panning) {
                panning = false
            }
        }

        onPositionChanged: {
            if (zooming) {
                selection.width = Math.abs(mouse.x - storedXPosition)
                selection.height = Math.abs(mouse.y - storedYPosition)

                if (mouse.x > storedXPosition) {
                    selection.x = storedXPosition
                } else {
                    selection.x = storedXPosition - selection.width
                }

                if (mouse.y > storedYPosition) {
                    selection.y = storedYPosition
                } else {
                    selection.y = storedYPosition - selection.height
                }
            }

            if (panning) {
                position.x += mouse.x - previousXPosition
                position.y += mouse.y - previousYPosition
                previousXPosition = mouse.x
                previousYPosition = mouse.y
            }
        }

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
                mouseEnabled: false
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
                source: 'demo://scope_1'

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
