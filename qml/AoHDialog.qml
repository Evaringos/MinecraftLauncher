import QtQuick 2.15
import QtQuick.Controls 2.15
// import QtGraphicalEffects
import QtQuick.Effects
import Qt5Compat.GraphicalEffects
import QtQuick.Layouts

Rectangle {
    id: root
    anchors.centerIn: parent.Center
    width: parent.width
    height: parent.height
    color: Theme.dialogDarkness
    radius: Theme.borderRadius
    visible: false


    MouseArea { // чтобы клики мыши не проходили сквозь окно
        anchors.fill: parent
        enabled: true
    }

    ColumnLayout {
        anchors.fill: parent
        Rectangle  {
            id: frame
            Layout.alignment: Qt.AlignCenter
            Layout.topMargin: Theme.toolbarHeight
            width: mainWindow.width - 60
            height: mainWindow.height - 60 - Theme.toolbarHeight
            border.width: Theme.borderWidth
            border.color: Theme.dialogBorderColor
            radius: Theme.borderRadius
            color: Theme.accentCol
            AoHButton {
                anchors {
                    top: parent.top
                    right: parent.right
                    topMargin: Theme.borderWidth
                    rightMargin: Theme.borderWidth
                }
                iconSource: "../cache/icons/close.svg"
                borderwidth: 0
                rectBorderRadius: 8
                onClicked: disappearAnimation.start()
            }
        }
    }
    // Анимация появления
    OpacityAnimator {
        id: appearAnimation
        target: root
        from: 0
        to: 1
        duration: 300  // Длительность анимации в миллисекундах
        running: false  // Анимация не запускается автоматически
    }
    // Анимация исчезновения
    OpacityAnimator {
        id: disappearAnimation
        target: root
        from: 1
        to: 0
        duration: 300  // Длительность анимации в миллисекундах
        running: false  // Анимация не запускается автоматически
        onFinished: root.visible = false
    }
    function appear(){
        root.visible = true
        root.opacity = 0
        appearAnimation.start()
    }
}
