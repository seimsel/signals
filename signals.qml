import QtQuick.Window 2.2
import QtQuick 2.14
import Signals 0.1

Window {
    visible: true

    Signal {
        id: renderer
        width: parent.width
        height: parent.height
        transform: [
            Scale { xScale: renderer.width; yScale: renderer.height/2 },
            Translate { y: renderer.height/2 }
        ]
    }
}
