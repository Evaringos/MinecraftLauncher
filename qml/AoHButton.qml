import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects




ToolButton {
    id: root

    function addAlpha(color, alpha) {
            var c = Qt.color(color);
            return Qt.rgba(c.r, c.g, c.b, alpha);
        }


    // ICON
    property string iconSource: ""
    property color iconColor: Theme.buttonIconColor
    property int   iconSize: Theme.buttonIconSize
    property color pressIconColor: Theme.accentCol

    // RECTANGLE
    property int   rectSize: Theme.buttonSize
    property int   rectWidth: Theme.buttonSize
    property int   rectHeight: Theme.buttonSize
    property int   rectBorderRadius: Theme.toolbarButtonRadius
    property alias borderwidth: rect.border.width
    //property alias leftsep: rect.leftseprect.width
    property bool leftsep: false
    property color rectBorderColor: Theme.accentColBright
    property color rectBGColor: Theme.buttonBackground
    property color hoverColor: Theme.accentColSemi
    property color pressColor: Theme.accentColBright
    property real bgOpacity: 1.0

    // TEXT
    property string title: ""
    property int   textSize: 14
    property color textColor: Theme.accentColBright
    property color textPressColor: Theme.accentCol
    //property color hoverIconColor: Theme.accentCol



    background: Rectangle {
            id: rect
            implicitWidth: root.rectWidth
            implicitHeight: root.rectHeight
            color: (root.down | root.checked ) ? root.pressColor :
                   (root.hovered ? root.hoverColor : addAlpha(root.rectBGColor, bgOpacity))
            border.color: root.down ? Qt.darker(color, 1.1) : rectBorderColor
            border.width: 1
            radius: rectBorderRadius

            Behavior on color {
                ColorAnimation { duration: 150 }
            }
    }

    contentItem: Item {
            implicitWidth: row.width
            implicitHeight: row.height

            Row {
                id: row
                anchors.centerIn: parent
                spacing: root.iconSource && root.title ? 5 : 0 // Отступ между иконкой и текстом


                Item {
                    width: root.iconSource ? root.iconSize : 0
                    height: root.iconSize
                    visible: root.iconSource !== ""


                    Image {
                        id: icon
                        source: root.iconSource
                        sourceSize: Qt.size(root.iconSize, root.iconSize)
                        visible: false // Делаем оригинальное изображение невидимым
                        anchors.centerIn: parent
                    }

                    ColorOverlay {
                        anchors.fill: icon
                        source: icon
                        color: (root.down | root.checked ) ? root.pressIconColor : root.iconColor
                        antialiasing: true
                    }
                }

                Text {
                    text: root.title
                    color: root.down ? root.textPressColor : root.textColor
                    font.pixelSize: textSize // Настройте по необходимости
                    anchors.verticalCenter: parent.verticalCenter
                    visible: root.title !== ""
                }
            }
        }

        states: [
            State {
                name: "hovered"
                when: root.hovered && !root.down
                PropertyChanges { target: root; scale: 1.01 }
            },
            State {
                name: "pressed"
                when: root.down
                PropertyChanges { target: root; scale: 0.99 }
            }
        ]

        transitions: Transition {
            NumberAnimation { properties: "scale"; duration: 20 }
        }
}
