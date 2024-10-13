import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtQuick.Effects
import QtMultimedia
import QtQuick.Window

Rectangle {
    property int borderradius: 8
    property string bordercolor: "#7b1dc9"
    property int spacerabovelogo: 1
    property string iconcolor: "#000000"
    property color toolbarcolor: bordercolor

    id: root
    //anchors.fill: parent
    anchors.centerIn: parent
    width: parent.width
    height: parent.height
    color: "transparent"
    AoHToolbar { id: aohToolbar }

    Rectangle { id: rootbg; anchors.fill: root; radius: borderradius; color: "black"}

    // DropShadow {
    //     anchors.fill: root
    //     spread: 0.3
    //     radius: 9
    //     cached: true
    //     samples: 15
    //     source: rootbg
    //     color: "#80000000"}


    MediaPlayer {
        id: mediaPlayer
        autoPlay: true
        source: "../cache/aoh_cut_resize.mp4"
        videoOutput: aohbg
        loops: MediaPlayer.Infinite
    }



    VideoOutput {
        id: aohbg
        anchors.fill: parent
        anchors.margins: parent.border.width
        property bool rounded: true
        layer.enabled: rounded
        layer.effect: OpacityMask {
            maskSource: Item {
                width: aohbg.width
                height: aohbg.height
                Rectangle {
                    anchors.centerIn: parent
                    width: aohbg.width
                    height: aohbg.height
                    radius: borderradius
                }
            }
        }
    }

    Column   {
        z:1
        Rectangle {// toolbarbg
            id: toobarbg
            width: root.width
            height: Theme.toolbarHeight

            topLeftRadius : borderradius
            topRightRadius : borderradius
            color: Theme.toolbarBackground
        }
        // Rectangle { // line under toolbar
        //     width: root.width
        //     height: Theme.borderWidth
        //     color: Theme.borderColor
        // }
}

    MultiEffect {
        anchors.fill: aohbg
        source: aohbg
        blurEnabled: true
        blurMax: Theme.bgBlur
        blur: 1.0
        property bool rounded: true
        layer.enabled: rounded
        layer.effect: OpacityMask {
            maskSource: Item {
                width: aohbg.width
                height: aohbg.height
                Rectangle {
                    anchors.centerIn: parent
                    width: aohbg.width
                    height: aohbg.height
                    radius: borderradius
                }
            }
        }
    }



    Rectangle {
        // Рамка вокруг окна
        id: frame_border
        z:2

        anchors.fill: aohFrame
        border.width: Theme.borderWidth

        color: "transparent"
        border.color: Theme.borderColor
        radius: borderradius
    }



    AoHContent { id: aohContent }

}


