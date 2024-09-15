import sys
import os
import AoHLauncher
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
from ConfigHandler import update_config, read_config, create_default_config
import ConfigHandler


Console92 = True
AoHClassic = False
config = read_config()

# def Icon():
#     icon_path = os.path.join(os.path.dirname(__file__), 'cache')
    
#     return QIcon(icon_path)

class DraggableStretchWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._drag_start_pos = None
        self._window_pos_at_drag_start = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_pos = event.globalPos()
            self._window_pos_at_drag_start = self.parentWidget().parentWidget().pos()

    def mouseMoveEvent(self, event):
        if self._drag_start_pos is not None:
            delta = event.globalPos() - self._drag_start_pos
            new_pos = self._window_pos_at_drag_start + delta
            self.parentWidget().parentWidget().move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_pos = None
            self._window_pos_at_drag_start = None

class Ui_MainWindow(object):
    def __init__(self):
        self.settings = QtCore.QSettings("AoH Launcher", "Settings")

    def launch_game_pressed(self):
        MainWindow.hide()
        # if sys.platform == 'win32':
        #     CREATE_NO_WINDOW = 0x08000000
        # else:
        #     CREATE_NO_WINDOW = 0
        AoHLauncher.launch_game(self.Username.text())
        MainWindow.show()

    def save_username_and_exit(self):
        update_config("Launcher", "Username", self.Username.text())
        MainWindow.close()

    def setupUi(self, MainWindow):
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache', 'aoh_icon.ico'))
        app_icon = QtGui.QIcon(icon_path)
        app.setWindowIcon(app_icon)
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("AoH Launcher")
        # QtWidgets.QApplication.setWindowIcon(QtGui.QIcon(os.path.join('cache', 'aoh_logo_256.png')))
        # MainWindow.setWindowIcon(Icon())
        # QtWidgets.QApplication.setWindowIcon(Icon())
        MainWindow.resize(500, 595)
        MainWindow.setMinimumSize(QtCore.QSize(500, 595))
        MainWindow.setMaximumSize(QtCore.QSize(500, 595))
        MainWindow.setStyleSheet("QWidget { background-color: #191919; color: #f2b036; }")
        # Add shadow
        # MainWindow.QtWidgets.QGraphicsDropShadowEffect(self)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 0, 10, 10)
        self.verticalLayout.setSpacing(5)

        # Toolbar
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(self.toolbar)
        self.toolbar.setContentsMargins(0, 0, 0, 0)
        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(32)
        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu) # Отключение встроенной функции удаления тулбара
        self.toolbar.setStyleSheet("""
            QToolBar {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #333333, stop:1 #000000);
            }
        """)

        # Иконки для кнопок
        icon_paths = {
            "close": os.path.join(os.path.dirname(__file__), 'cache', 'close.png'),
            "settings": os.path.join(os.path.dirname(__file__), 'cache', 'settings.png'),
            "hide": os.path.join(os.path.dirname(__file__), 'cache', 'hide.png'),
            "folder": os.path.join(os.path.dirname(__file__), 'cache', 'folder.png'),
            "refresh": os.path.join(os.path.dirname(__file__), 'cache', 'folder.png')
        }
        game_folder_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')

        # Настройка кнопки Settings
        self.SettingsButton = QtWidgets.QPushButton()
        self.SettingsButton.setFixedSize(32, 32)
        self.SettingsButton.setIcon(QIcon(icon_paths["settings"]))
        self.toolbar.addWidget(self.SettingsButton)
        # Создаем выпадающее меню
        self.settings_menu = QtWidgets.QMenu(MainWindow)
        self.theme_menu = QtWidgets.QMenu("Themes settings", self.settings_menu)
        self.theme_menu.setIcon(QIcon(icon_paths["settings"]))
        self.language_menu = QtWidgets.QMenu("Language settings", self.settings_menu)
        #self.language_menu.setIcon(QIcon(icon_paths["settings"]))
        # Создаем действия для меню
        self.theme_option1 = self.theme_menu.addAction("Console92")
        self.theme_option2 = self.theme_menu.addAction("AoH Classic")
        self.language_option1 = self.language_menu.addAction("English")
        self.language_option2 = self.language_menu.addAction("Русский")
        self.theme_option1.setCheckable(True)
        self.theme_option2.setCheckable(True)
        self.language_option1.setCheckable(True)
        self.language_option2.setCheckable(True)
        # Подключаем слоты для действий
        self.theme_option1.toggled.connect(lambda: self.on_theme_option_toggled(self.theme_option1))
        self.theme_option2.toggled.connect(lambda: self.on_theme_option_toggled(self.theme_option2))
        self.language_option1.toggled.connect(lambda: self.on_theme_option_toggled(self.language_option1))
        self.language_option2.toggled.connect(lambda: self.on_theme_option_toggled(self.language_option2))
        # Добавляем вложенное меню в основное меню
        self.settings_menu.addMenu(self.theme_menu)
        self.settings_menu.addMenu(self.language_menu)
        self.settings_menu.addAction("Credits")
        # Привязываем меню к кнопке
        self.SettingsButton.setMenu(self.settings_menu)

        # Папка с игрой
        self.FolderWithGame = QtWidgets.QPushButton()
        self.FolderWithGame.setFixedSize(32, 32)
        self.FolderWithGame.setIcon(QIcon(icon_paths["folder"]))
        self.toolbar.addWidget(self.FolderWithGame)
        # Метод для открытия папки
        def open_folder():
            QDesktopServices.openUrl(QUrl.fromLocalFile(game_folder_path))
        # Подключение метода к нажатию кнопки
        self.FolderWithGame.clicked.connect(open_folder)

        # Обновление модов (возможно временная функция)
        self.Refresh = QtWidgets.QPushButton()
        self.Refresh.setFixedSize(32, 32)
        self.Refresh.setIcon(QIcon(icon_paths["refresh"]))
        self.toolbar.addWidget(self.Refresh)

        # def refresh_mods():

        # self.Refresh.clicked.connect(refresh_mods)

        # Stretch
        stretch_widget = DraggableStretchWidget()
        self.toolbar.addWidget(stretch_widget)
        # Hide window button
        self.HideWindow = QtWidgets.QPushButton()
        self.HideWindow.setFixedSize(32, 32)
        self.HideWindow.setIcon(QIcon(icon_paths["hide"]))
        self.HideWindow.clicked.connect(MainWindow.showMinimized)
        self.toolbar.addWidget(self.HideWindow)
        # Close window button
        self.CloseWindow = QtWidgets.QPushButton()
        self.CloseWindow.setFixedSize(32, 32)
        self.CloseWindow.setIcon(QIcon(icon_paths["close"]))
        self.CloseWindow.clicked.connect(self.save_username_and_exit)
        self.toolbar.addWidget(self.CloseWindow)

        # Launcher logo
        Launcher_logo = os.path.join(os.path.dirname(__file__), 'cache', 'Launcher_logo.png')
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setObjectName("image_label")
        self.image_label.setPixmap(QtGui.QPixmap(Launcher_logo))
        self.image_label.setScaledContents(True)  # Включаем масштабирование
        self.image_label.resize(100, 100)  # Устанавливаем размеры
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # Выравниваем картинку по центру
        self.verticalLayout.addWidget(self.image_label)

        # Spacer
        #spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        #self.verticalLayout.addItem(spacerItem)

        # Лист последних обновлений лаунчера
        self.Whattsnew = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Whattsnew.sizePolicy().hasHeightForWidth())
        self.Whattsnew.setSizePolicy(sizePolicy)
        self.Whattsnew.setMinimumSize(QtCore.QSize(0, 210))
        self.Whattsnew.setObjectName("Whattsnew")
        self.verticalLayout.addWidget(self.Whattsnew)
        self.Whattsnew.setStyleSheet("border-radius: 5px; border: 1px solid rgb(8, 8, 8); background-color: #1C1C1C;")

        # Spacer
        spacerItem1 = QtWidgets.QSpacerItem(100, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)

        # Поле ввода Username
        self.Username = QtWidgets.QLineEdit(self.centralwidget)
        self.Username.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Username.sizePolicy().hasHeightForWidth())
        self.Username.setSizePolicy(sizePolicy)
        self.Username.setMinimumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(12)
        self.Username.setFont(font)
        self.Username.setDragEnabled(False)
        self.Username.setReadOnly(False)
        self.Username.setClearButtonEnabled(False)
        self.Username.setText(config["Launcher"]["Username"])
        self.verticalLayout.addWidget(self.Username)        
#        self.Username.textChanged.connect(self.save_username)
        # self.Username.setStyleSheet("border-radius: 5px; border: 1px solid rgb(51, 51, 51); background-color: #CCCCCC; padding: 2px; color: #000000;")
        self.Username.setStyleSheet("""
            QLineEdit {
                border-radius: 5px;
                border: 1px solid rgb(8, 8, 8);
                background-color: #1C1C1C;
                padding: 2px;
                font-family: 'Consolas', monospace;
                /* font-size: 14px; */
                color: #f2b036;
            }
        """)
        
        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        # Кнопка запуска игры Play button
        self.PlayButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlayButton.setMinimumSize(QtCore.QSize(150, 40))
        self.PlayButton.setObjectName("PlayButton")
        self.PlayButton.setText("Play")
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setPointSize(18)
        font.setWeight(QtGui.QFont.Bold)  # или font.setWeight(75) для более тонкого шрифта
        self.PlayButton.setFont(font)
        self.PlayButton.clicked.connect(self.launch_game_pressed)  
        self.verticalLayout.addWidget(self.PlayButton)
        # self.PlayButton.setStyleSheet("font-family: 'Consolas', monospace; font-size: 18px;")
        self.PlayButton.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                border: 1px solid rgb(8, 8, 8);
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
                border: 1px solid rgb(50, 50, 50);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #333333, stop: 1 #2B2B2B);
                border: 1px solid rgb(100, 100, 100);
            }
        """)

        # Progress bar устаноки игры
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setVisible(True) # Видимость progress bar
        self.progressBar.setMinimumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.progressBar.setFont(font)
        self.progressBar.setAcceptDrops(False)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgb(8, 8, 8);
                border-radius: 5px;
                background-color: rgb(50, 50, 50);
            }
            QProgressBar::chunk {
                background-color: #f2b036;
                border-radius: 5px;
            }
        """)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Launcher Translate
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Username.setPlaceholderText(_translate("MainWindow", "Username:"))
        # self.patchButton.setText(_translate("MainWindow", "patchButton"))
        # self.FolderWithGame.setText(_translate("MainWindow", "folderButton"))
        # self.PlayButton.setText(_translate("MainWindow", "Play"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


        # self.centralwidget.setStyleSheet("border-radius: 10px;")
        # app.setStyleSheet("border-radius: 10px;")
