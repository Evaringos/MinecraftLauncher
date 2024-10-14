// Theme.qml
pragma Singleton
import QtQuick

QtObject { // blue theme
    property color accentCol: "#023E7A"
    property color accentColSemi: "#378DBD"
    property color accentColBright: "#6BDCFF"
    property color accentBgSemi: "#80023E7A"

    property int   bgBlur: 32
    property int   borderWidth: 2
    property int   borderRadius: 8

    property color borderColor: accentCol

    property color consoleBackground: "#80000000"

    property color toolbarBackground: borderColor
    property int   toolbarButtonRadius: 4
    property int   toolbarHeight: 30

    property int   buttonSize: 10
    property int   buttonIconSize: 15
    property color buttonBackground: accentCol
    property color buttonIconColor: accentColBright

    property color buttonHoverBackground: "#404040"
    property color buttonPressBackground: "#505050"
    property color buttonText: "#f0f0f0"
    property color buttonHoverText: "#ffffff"
    property color buttonPressText: "#ffffff"

    // Menu properies
    property int menuHoveredPad: (Theme.borderWidth * 2)
    property int menuArrowSize: Theme.buttonIconSize / 2
    property int menuWidth: 100

    function toggleTheme() {
        themeName = themeName === "light" ? "dark" : "light"
    }
}
