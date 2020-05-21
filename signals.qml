import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Dialogs 1.0

import Matplotlib 0.1

ApplicationWindow {
    visible: true

    width: 800
    height: 600

    menuBar: MenuBar {
        Menu {
            title: qsTr('&File')
            Action {
                text: qsTr('&Open...')
                onTriggered: {
                    fileDialog.open()
                }
            }
        }
    }

    FileDialog {
        id: fileDialog

        nameFilters: [
            'CSV files (*.csv *.txt)'
        ]
        selectMultiple: false
        selectFolder: false

        onAccepted: {
            controller.open(fileDialog.fileUrl)
        }
    }

    FigureCanvas {
        id: canvas
        anchors.fill: parent

        Component.onCompleted: {
            controller.setCanvas(canvas)
        }
    }
}
