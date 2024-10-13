import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Effects
import Qt5Compat.GraphicalEffects

Rectangle {
    z:3
    anchors.top: parent.top
    height: Theme.toolbarHeight
    width: root.width
    color: "transparent"

    MouseArea { // Область для перемещения окна
        property point clickPos: "0,0"
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        onPressed: function(mouse) {
            if (mouse.button === Qt.LeftButton) {
                clickPos = Qt.point(mouse.x, mouse.y) }}
        onPositionChanged: function(mouse) {
            if (mouse.buttons & Qt.LeftButton) {
                var delta = Qt.point(mouse.x - clickPos.x, mouse.y - clickPos.y)
                mainWindow.x += delta.x ; mainWindow.y += delta.y}}}

    RowLayout {
        id: grid
        anchors.fill: parent
        Layout.alignment: Qt.AlignCenter
        spacing: 0

        AoHButton {
            id: settingsMenu
            checkable: true
            onClicked: { menu.open(); enabled = !enabled }
            borderwidth: 0
            Layout.leftMargin: Theme.borderWidth
            iconSource: "../cache/icons/cogwheel.svg"

            AoHMenu {
                id: menu
                width: 180
                borderradius: Theme.borderRadius
                AoHMenu {
                    icon.source: "../cache/icons/brush.svg"
                    borderradius: Theme.borderRadius
                    title: "Theme settings"

                    ActionGroup{ id: themes }
                    Action{ checkable: true ; ActionGroup.group: themes ; text:"AoHClassic"}
                    Action{ checkable: true ; ActionGroup.group: themes ; text:"Classic92"}
                    Action{ checkable: true ; ActionGroup.group: themes ; text:"Gruvbox"}
                    }

                AoHMenu{
                    title: "Language settings"
                    icon.source: "../cache/icons/globe.svg"
                    borderradius: Theme.borderRadius

                    ActionGroup{ id: languages }
                    Action{ checkable: true ; ActionGroup.group: languages ; text:"English"}
                    Action{ checkable: true ; ActionGroup.group: languages ; text:"Русский"}
                }
                AoHMenu {
                    title: "Amount of RAM"
                    icon.source: "../cache/icons/memory.svg"
                    borderradius: Theme.borderRadius

                    ActionGroup{ id: ram }
                    Action{ checkable: true ; ActionGroup.group: ram ; text:"2 Gb"}
                    Action{ checkable: true ; ActionGroup.group: ram ; text:"4 Gb"}
                    Action{ checkable: true ; ActionGroup.group: ram ; text:"8 Gb"}
                    Action{ checkable: true ; ActionGroup.group: ram ; text:"12 Gb"}
                    Action{ checkable: true ; ActionGroup.group: ram ; text:"18 Gb"}
                }
                Action {
                    text: "Credits"
                    icon.source: "../cache/icons/info.svg"
                    onTriggered: bridge.credits()
                }
                Action {
                    text: "Delete Minecraft"
                    icon.source: "../cache/icons/bin.svg"
                    onTriggered: bridge.deleteMinecraft()
                }
            }
        }

        AoHToolBarSeparator {}

        AoHButton {
            iconSource: "../cache/icons/folder.svg"
            onClicked: bridge.open_folder()
            borderwidth: 0
        }

        AoHToolBarSeparator {}

        AoHButton {
            iconSource: "../cache/icons/telegram.svg"
            onClicked: bridge.openTelegram()
            borderwidth: 0}

        AoHToolBarSeparator {}

        AoHButton {
            iconSource: "../cache/icons/reload.svg"
            borderwidth: 0}

        AoHToolBarSeparator {}

        Item { Layout.fillWidth: true }

        //right side
        AoHToolBarSeparator {}

        AoHButton {
            id: toolbar_hideButton
            borderwidth: 0
            icon.color: iconcolor
            iconSource: "../cache/icons/hide2.svg"
            onClicked: mainWindow.showMinimized()
        }

        AoHToolBarSeparator {}

        AoHButton {
            id: toolbar_closeButton
            borderwidth: 0
            Layout.rightMargin: Theme.borderWidth
            icon.color: iconcolor
            iconSource: "../cache/icons/close2.svg"
            onClicked: mainWindow.close()
        }
    }
}
