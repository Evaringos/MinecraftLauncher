from PyQt5 import QtWidgets

# AoHClassic
# ColAccent = "#f2b036"
# ColBg = "#eaeaea"

# Classic92
# ColAccent = "#f2b036"
# ColBg = "#191919"


class ThemeNew(QtWidgets.QMainWindow):
    def __init__(self):
        super(ThemeNew,self).self.__init__()

    def SetTheme(self, theme):
        if theme == "Classic92": ThemeNew.Classic92(self)
        elif theme == "AoHClassic": ThemeNew.AoHClassic(self)

    def AoHClassic(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f1f1f1;
        }
        QMenu { /*Dropdown menu*/
            background-color: #f1f1f1;
            color: #f2b036;
        }
        QToolBar {
            border: none;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #d0d0d0, stop:1 #ffffff);
        }
        QLineEdit { /* Username input area */
            border-radius: 5px;
            border: 1px solid #ffffff;
            background-color: #f1f1f1;
            padding: 2px;
            font-family: 'Consolas', monospace;
            /* font-size: 14px; */
            color: #f2b036;
        }
        QListView { /* Console box*/
            border-radius: 5px;
            border: 1px solid #ffffff;
            background-color: #f1f1f1;
            color: #f2b036;
        }
        QPushButton {
            border-radius: 5px;
            border: 1px solid #ffffff;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f1f1f1, stop: 1 #e9e9e9);
            padding: 2px;
            font-family: 'Consolas', monospace;
            font-size: 18px;
            font-weight: bold;
            color: #f2b036;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f1f1f1, stop: 1 #e0e0e0);
            border: 1px solid #f1f1f1;
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #f1f1f1, stop: 1 #e9e9e9);
            border: 1px solid #e9e9e9;
        }
        QProgressBar {
            border: 1px solid #ffffff;
            border-radius: 5px;
            background-color: #e9e9e9;
        }
        QProgressBar::chunk {
            background-color: #f2b036;
            border-radius: 5px;
        }
        QToolTip {
            background-color : #f1f1f1;
            color: #f2b036;
            border: none;
        }
        QLabel#image_label {
            qproperty-pixmap: url("cache/Launcher_logo_dark.png");
            qproperty-scaledContents: true;
        }
        """)
        
    def Classic92(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #191919;
        }
        QMenu { /*Dropdown menu*/
            background-color: #191919;
            color: #f2b036;
        }
        QToolBar {
            border: none;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #333333, stop:1 #000000);
        }
        QLineEdit { /* Username input area */
            border-radius: 5px;
            border: 1px solid #080808;
            background-color: #191919;
            padding: 2px;
            font-family: 'Consolas', monospace;
            /* font-size: 14px; */
            color: #f2b036;
        }
        QListView { /* Console box*/
            border-radius: 5px;
            border: 1px solid #080808;
            background-color: #1C1C1C;
            color: #f2b036;        
        }
        /*Play Button*/
        QPushButton {
            border-radius: 5px;
            border: 1px solid #080808;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1C1C1C, stop: 1 #151515);
            padding: 2px;
            font-family: 'Consolas', monospace;
            font-size: 18px;
            font-weight: bold;
            color: #f2b036;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2B2B2B, stop: 1 #333333);
            border: 1px solid #323232;
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #333333, stop: 1 #2B2B2B);
            border: 1px solid #646464;
        }
        QProgressBar {
            border: 1px solid rgb(8, 8, 8);
            border-radius: 5px;
            background-color: rgb(50, 50, 50);
        }
        QProgressBar::chunk {
            background-color: #f2b036;
            border-radius: 5px;
        }
        QToolTip {
            background-color : #1c1c1c;
            color: #f2b036;
            border: none;
        }
        QLabel#image_label {
            qproperty-pixmap: url("cache/Launcher_logo.png");
            qproperty-scaledContents: true;
        }
        """)
        


    
    


