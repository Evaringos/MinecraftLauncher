import QtQuick
import QtQuick.Controls 2.3
import Qt5Compat.GraphicalEffects


Menu {
    property int borderradius
    property int iconSize: Theme.buttonIconSize

    id:root
    x: parent.x - 2
    y: parent.y + parent.height - 2
    overlap: 0

    onClosed: {
        parent.checked = !parent.checked
        parent.enabled = true
    }

    delegate: MenuItem {
        id:menuItem
        implicitWidth: 240
        implicitHeight: 20

        arrow: Rectangle {
            id: arrowGroup
            width:  10
            height: 10
            anchors.verticalCenter: menuItem.verticalCenter
            anchors.right: menuItem.right
            color: "transparent"
            visible: menuItem.subMenu ? true : false
            Image {
                id: arrowShape
                anchors.fill: arrowGroup
                anchors.verticalCenter: arrowGroup.verticalCenter
                source: "../cache/icons/chevron.svg"
                sourceSize: Qt.size(iconSize, iconSize)
                visible: false
            }
            ColorOverlay {
                anchors.fill: arrowShape
                source: arrowShape
                color: Theme.accentColBright
            }
        }

        indicator: Item {
            id: indicatorGroup
            anchors.verticalCenter: menuItem.verticalCenter
            anchors.left: menuItem.left
            anchors.leftMargin:  menuItem.hovered ? (Theme.borderWidth + Theme.menuHoveredPad) : (Theme.borderWidth * 2)
            height: iconSize - 2
            width:  iconSize - 2
            Rectangle {
                width: indicatorGroup.width
                height: indicatorGroup.width
                anchors.centerIn: parent
                color: "transparent"
                visible: menuItem.checkable
                border.color: Theme.accentColBright
                radius: Theme.toolbarButtonRadius
                Rectangle {
                    width: indicatorGroup.width - 6
                    height: indicatorGroup.width - 6
                    anchors.centerIn: parent
                    visible: menuItem.checked
                    color: Theme.accentColBright
                    radius: Theme.toolbarButtonRadius
                }
            }
        }


        contentItem: Row {
            anchors.fill: menuItem
            spacing: Theme.borderWidth
            leftPadding: menuItem.hovered ? Theme.menuHoveredPad : Theme.borderWidth
            // Item {
            //     width: menuItem.checked ? indicatorGroup.width : 0
            //     height: menuItem.height
            // }
            Rectangle {
                id: iconContainer
                width: iconSize
                height: iconSize
                anchors.verticalCenter: parent.verticalCenter

                color: "transparent"
                visible: (menuItem.icon.source != "") ? true : false
                Image {
                    id: iconShape
                    anchors.verticalCenter: parent.verticalCenter
                    source: menuItem.icon.source
                    sourceSize: Qt.size(iconSize, iconSize)
                    visible: false
                }
                ColorOverlay {
                    anchors.fill: iconShape
                    source: iconShape
                    color: Theme.accentColBright
                }
            }

            Text {
                id: text
                text: menuItem.text
                padding: menuItem.checkable ? 18 : 0//indicatorGroup.width : 0
                //font.family: "Courier New"
                antialiasing: true
                // font.styleName: "Regular"
                font.pixelSize: 12
                anchors.verticalCenter: parent.verticalCenter
                verticalAlignment: Text.AlignVCenter
                color: Theme.accentColBright
            }
        }

        background: Rectangle {
            implicitHeight: parent.implicitHeight
            implicitWidth: parent.implicitWidth
            topLeftRadius: (currentIndex === 0) ? borderradius : 0
            bottomLeftRadius: (currentIndex === (count - 1) ) ? borderradius : 0
            topRightRadius: topLeftRadius
            bottomRightRadius: bottomLeftRadius
            color: menuItem.hovered ? Theme.accentColSemi : "transparent"
        }
    }

    background: Rectangle {
        id: menubgrect
        implicitWidth: 120
        implicitHeight: 20
        color: Theme.accentCol
        border.color: Theme.accentColBright
        radius: borderradius
    }
}
