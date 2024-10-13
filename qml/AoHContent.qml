import QtQuick 2.15
import QtQuick.Layouts
import QtQuick.Controls 2.15
import Qt5Compat.GraphicalEffects

ColumnLayout {
    id: root
    height: aohFrame.height
    width: aohFrame.width
    anchors.fill: parent
    Layout.topMargin: Theme.toolbarHeight

    //Layout.bottomMargin: 30

    Image {
        id: aohlogo
        Layout.preferredWidth: parent.width
        Layout.preferredHeight: 200
        source: "../cache/Launcher_logo_dark.png"
        autoTransform: false
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        id: consolebox
        border.color: Theme.accentColBright
        border.width: Theme.borderWidth
        Layout.minimumWidth: parent.width - 30 * 2
        Layout.leftMargin: 30
        height: 220
        radius: borderradius
        color: Theme.consoleBackground

        ListView {
            id: listView
            anchors.fill: parent
            width: parent.width
            height: parent.height
            model: consoleModel  // Используем модель из Python
            delegate: Text {
                leftPadding: 8
                width: parent.width
                text: model.text  // Используем 'text' вместо 'name'
                color: Theme.accentColBright
                wrapMode: Text.Wrap
            }
        }
    }

    Row {
        id: yar
        spacing: 10
        leftPadding: 30
        height: 40

        Rectangle {
            id: textRect
            border.width: Theme.borderWidth
            radius: Theme.borderRadius
            border.color: Theme.accentColBright
            color: Theme.accentBgSemi
            height: parent.height
            width: 215
            TextInput {
                id: textField
                //anchors.fill: parent
                //leftPadding: 8
                width: textRect.width
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 22
                font.family: "Consolas"
                color: Theme.accentColBright

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    font: parent.font
                    color: Theme.accentColSemi
                    text: "Username"
                    visible: !parent.text
                }
            }
        }
        AoHButton {
            id: accountRect
            borderwidth: Theme.borderWidth
            rectBorderRadius: Theme.borderRadius
            //bordercolor: Theme.accentColBright
            //color: Theme.accentBgSemi
            height: parent.height
            width: 215
            bgOpacity: 0.5
            iconSource: "../cache/icons/account.svg"
            title: qsTr("Account")
        }
    }

    AoHButton { // Play button
        id: playButtonObj
        //rectBGColor: Theme.accentBgSemi
        title: playButton.playButtonText
        textSize: 20
        borderwidth: 2
        bgOpacity: 0.5
        rectBorderRadius: 8
        Layout.alignment: Qt.AlignHCenter
        rectWidth: parent.width - 30 * 2
        rectHeight: 40
        onClicked: playButton.play_pressed()
        Layout.bottomMargin: 30
    }
}
