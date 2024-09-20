from PyQt5 import QtWidgets, QtCore # Добавил QtCore

# AoHClassic
# ColAccent = "#f2b036"
# ColBg = "#eaeaea"

# Classic92
# ColAccent = "#f2b036"
# ColBg = "#191919"


class ThemeNew(QtWidgets.QMainWindow):
    def __init__(self):
        super(ThemeNew,self).self.__init__()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)  # Set the timer to fire every 50ms
        
    def SetTheme(self, theme):
        if theme == "Classic92": ThemeNew.Classic92(self)
        elif theme == "AoHClassic": ThemeNew.AoHClassic(self)

    def AoHClassic(self):
        self.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x0:1, y2:1, 
            stop:0 #2f0552, stop:1 #200338);
        }
        QMenu { /*Dropdown menu*/
            background-color: #330d52;
            border: 1px solid #7d1dcc;                           
            color: #b17dff;
        }
        QMenu:hover { /*Dropdown menu*/              
            color: #601fc2;
        }
        QToolBar {
            border: none;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #2f0552, stop:1 #7d1dcc);
        }
        QLineEdit { /* Username input area */
            border-radius: 5px;
            border: 1px solid #7d1dcc;
            background-color: #3a0d5e;
            padding: 2px;
            font-family: 'Consolas', monospace;
            /* font-size: 14px; */
            color: #b17dff;
        }
        QListView { /* Console box*/
            border-radius: 5px;
            border: 1px solid #7d1dcc;
            background-color: #3a0d5e;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #2b0847, stop:1 #3a0d5e);                           
            color: #b17dff;
        }
        QPushButton {
            border-radius: 5px;
            border: 2px solid #7d1dcc;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #2b0847, stop: 1 #3a0d5e);
            padding: 2px;
            font-family: 'Consolas', monospace;
            font-size: 18px;
            font-weight: bold;
            color: #b17dff;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #61199c, stop: 1 #601fc2);
            border: 1px solid #61199c;
        }
        QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #61199c, stop: 1 #2f0552);
            border: 1px solid #61199c;
        }
        QProgressBar {
            border: 1px solid #7d1dcc;
            border-radius: 5px;
            background-color: #601fc2;
        }
        QProgressBar::chunk {
            background-color: #b17dff;
            border-radius: 5px;
        }
        QToolTip {
            background-color : #601fc2;
            color: #b17dff;
            border: none;
        }
        QLabel#image_label {
            qproperty-pixmap: url("cache/Launcher_logo_dark.png");
            qproperty-scaledContents: true;
        }
        QMenu::item:selected {
            background-color: #401463;
        }
        """)
        
    def Classic92(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #191919;
            border: 1px solid #000000;  /*Новая обводка, не знаю как ее сделать чуть ниже сверху и стоит ли сделать оранжевой?*/              
        }
        QMenu { /*Dropdown menu*/
            background-color: #191919;
            border: 1px solid #f2b036;                           
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
        QListWidget {
            font-family: 'Consolas';
            font-size: 14px;
            outline: 0;
        }
        QListWidget::item:hover {
            background: transparent;
        }
        QListWidget::item:selected {
            background: transparent;
            color: #f2b036; /* иначе сбросится */
            border: none;
        }
        QListWidget::item:focus {
            border: none;  /* Убирает границу фокуса для отдельных элементов */
        }
        QLabel#image_label {
            qproperty-pixmap: url("cache/Launcher_logo.png");
            qproperty-scaledContents: true;
        }
        QMenu::item:selected {
            background-color: #292828;
        }
        """)
