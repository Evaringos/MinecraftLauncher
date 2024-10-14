import QtQuick
import QtQuick.Window
import Qt5Compat.GraphicalEffects
import QtQuick.Controls

ApplicationWindow {
    id: mainWindow
    title: "AoH Launcher"
    width: 510
    height: 610
    flags: Qt.FramelessWindowHint | Qt.Window
    color: "transparent"
    visible: false



    Timer {
        id: showTimer
        running: true
        interval: 100
        repeat: false
        onTriggered: {
            mainWindow.visible = true
            //bridge.setFlags(mainWindow)
        }
    }
    Component.onCompleted: {
       bridge.setFlags(mainWindow)
    }

    AoHFrame {
         id: aohFrame
    }
}

