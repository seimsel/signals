import QtQuick.Window 2.2
import QtQuick 2.3
import Signals 0.1

Window {
    visible: true

    Signal {
        width: parent.width
        height: parent.height
    }
}
