import sys
import os
import GameLauncher
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QIcon, QDesktopServices, QPainter, QPixmap
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtSvg import QSvgRenderer
from ConfigHandler import update_config, read_config, create_default_config
from Themes import ThemeNew

config = read_config()

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

class NoClickModel(QtCore.QStringListModel):
    def flags(self, index):
        return QtCore.Qt.NoItemFlags

class Ui_MainWindow(object):
    def __init__(self):
        self.settings = QtCore.QSettings("AoH Launcher", "Settings")
        
    def update_theme(self, theme=None):
        # AoHClassic по дефолту
        if theme :
            ThemeNew.SetTheme(MainWindow,theme)
            update_config("Launcher", "Theme", theme)
        else: ThemeNew.SetTheme(MainWindow,config["Launcher"]["theme"])


    def launch_game_pressed(self):
        MainWindow.hide()
        GameLauncher.launch_game(self.Username.text())
        MainWindow.show()

    def save_username_and_exit(self):
        update_config("Launcher", "Username", self.Username.text())
        MainWindow.close()

    def setupUi(self, MainWindow):
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache', 'aoh_icon.ico'))
        app_icon = QtGui.QIcon(icon_path)
        app.setWindowIcon(app_icon)
        self.update_theme()
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) # отключение рамки окна

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("AoH Launcher")
        MainWindow.resize(500, 595)
        MainWindow.setMinimumSize(QtCore.QSize(500, 595))
        MainWindow.setMaximumSize(QtCore.QSize(500, 595))
        
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

        # Иконки для кнопок
        icon_paths = {
            "close": os.path.join('cache', 'icons', 'close.svg'),
            "settings": os.path.join('cache', 'icons', 'cogwheel.svg'),
            "hide": os.path.join('cache', 'icons', 'hide.svg'),
            "folder": os.path.join('cache', 'icons', 'folder.svg'),
            "refresh": os.path.join('cache', 'icons', 'reload.svg'),
            "globe": os.path.join('cache', 'icons', 'globe.svg'),
            "brush": os.path.join('cache', 'icons', 'brush.svg'),
            "info": os.path.join('cache', 'icons', 'info.svg')
        }
        game_folder_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')

        # Настройка кнопки Settings
        self.SettingsButton = QtWidgets.QPushButton()
        self.SettingsButton.setFixedSize(32, 32)
        self.SettingsButton.setIcon(QIcon(icon_paths["settings"]))
        self.toolbar.addWidget(self.SettingsButton)

        
        # Создаем выпадающее меню (dropdown menu)
        self.settings_menu = QtWidgets.QMenu(MainWindow)
        self.theme_menu = QtWidgets.QMenu("Themes settings", self.settings_menu)
        self.theme_menu.setIcon(QIcon(icon_paths["brush"]))
        
        self.language_menu = QtWidgets.QMenu("Language settings", self.settings_menu)
        self.language_menu.setIcon(QIcon(icon_paths["globe"]))

        self.Credits = QtWidgets.QAction("Credits", self.settings_menu)
        self.Credits.setIcon(QIcon(icon_paths["info"]))

        # Создаём группу действий для темы
        self.theme_menu_group = QtWidgets.QActionGroup(MainWindow)
        self.theme_menu_group.setExclusive(True)
        
        # Создаем действия для меню
        self.theme_option1 = self.theme_menu_group.addAction("AoH Classic")
        self.theme_option2 = self.theme_menu_group.addAction("Console92")

        self.theme_menu.addAction(self.theme_option1)
        self.theme_menu.addAction(self.theme_option2)        

        self.theme_option1.setCheckable(True)
        self.theme_option2.setCheckable(True)
        if config["Launcher"]["Theme"] == "AoHClassic": self.theme_option1.setChecked(True) #Галочка по дефолту
        else: self.theme_option2.setChecked(True)

        
        self.language_option1 = self.language_menu.addAction("English")
        self.language_option2 = self.language_menu.addAction("Русский")
        self.language_option1.setCheckable(True)
        self.language_option1.setChecked(True)
        self.language_option2.setCheckable(True)

        
        # Подключаем слоты для действий. triggered - действие только когда галка ставится
        self.theme_option1.triggered.connect(lambda: self.update_theme("AoHClassic"))
        self.theme_option2.triggered.connect(lambda: self.update_theme("Classic92"))
        self.language_option1.toggled.connect(lambda: self.on_theme_option_toggled(self.language_option1))
        self.language_option2.toggled.connect(lambda: self.on_theme_option_toggled(self.language_option2))
        self.Credits.triggered.connect(lambda: ShowCredits())
        
        # Добавляем вложенное меню в основное меню
        self.settings_menu.addMenu(self.theme_menu)
        self.settings_menu.addMenu(self.language_menu)
        self.settings_menu.addAction(self.Credits)

        def ShowCredits():
            self.add_message_to_console("""---================---
CEO of project - Scavenger (Evaringos)
Core programmer - Stradlater25
Designer / Community manager - Xeenomiya
---================---""")
        
        self.SettingsButton.setMenu(self.settings_menu) # Привязываем меню к кнопке
        self.SettingsButton.setToolTip("Settings")

        # Папка с игрой
        self.FolderWithGame = QtWidgets.QPushButton()
        self.FolderWithGame.setFixedSize(32, 32)
        self.FolderWithGame.setIcon(QIcon(icon_paths["folder"]))
        self.FolderWithGame.setToolTip("Open game folder")
        self.toolbar.addWidget(self.FolderWithGame)
        # Метод для открытия папки
        def open_folder():
            QDesktopServices.openUrl(QUrl.fromLocalFile(game_folder_path))
        # Подключение метода к нажатию кнопки
        self.FolderWithGame.clicked.connect(open_folder)

        # Обновление модов (возможно временная функция)
        self.Refresh = QtWidgets.QPushButton()
        self.Refresh.setToolTip("Reinstall mods")
        self.Refresh.setFixedSize(32, 32)
        self.Refresh.setIcon(QIcon(icon_paths["refresh"]))
        self.toolbar.addWidget(self.Refresh)

        # def refresh_mods():
        self.Refresh.clicked.connect(GameLauncher.cloudDownload)

        # Stretch
        stretch_widget = DraggableStretchWidget()
        self.toolbar.addWidget(stretch_widget)
        
        # Hide window button
        self.HideWindow = QtWidgets.QPushButton()
        self.HideWindow.setFixedSize(32, 32)
        self.HideWindow.setIcon(QIcon(icon_paths["hide"]))
        self.HideWindow.setToolTip("Hide")
        self.HideWindow.clicked.connect(MainWindow.showMinimized)
        self.toolbar.addWidget(self.HideWindow)
        # Close window button
        self.CloseWindow = QtWidgets.QPushButton()
        self.CloseWindow.setFixedSize(32, 32)
        self.CloseWindow.setIcon(QIcon(icon_paths["close"]))
        self.CloseWindow.setToolTip("Close")        
        self.CloseWindow.clicked.connect(self.save_username_and_exit)
        self.toolbar.addWidget(self.CloseWindow)

        # Launcher logo
        # Launcher_logo = os.path.join(os.path.dirname(__file__), 'cache', 'Launcher_logo.png')
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        # Консоль для более отзывчивого интерфейса
        self.Console = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Console.sizePolicy().hasHeightForWidth())
        self.Console.setSizePolicy(sizePolicy)
        self.Console.setMinimumSize(QtCore.QSize(0, 210))
        self.Console.setObjectName("Console")
        self.verticalLayout.addWidget(self.Console)

        # Модель данных для QListView
        self.model = QtGui.QStandardItemModel()
        self.Console.setModel(self.model)
        # Отключение обводки строк
        self.Console.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # Для выбора строк
        self.Console.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # Отключаем выбор
        # Стартовое сообщение
        self.add_message_to_console("Launcher started")

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

        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        # Кнопка запуска игры Play button
        self.PlayButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlayButton.setMinimumSize(QtCore.QSize(150, 40))
        self.PlayButton.setObjectName("PlayButton")
        self.PlayButton.setText("Play")
        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setPointSize(18)
        font.setWeight(QtGui.QFont.Bold)  # или font.setWeight(75) для более тонкого шрифта
        self.PlayButton.setFont(font)
        self.PlayButton.clicked.connect(self.launch_game_pressed)  
        self.verticalLayout.addWidget(self.PlayButton)

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

    def add_message_to_console(self, message):
        # Создаем новый элемент списка с заданным стилем
        item = QtGui.QStandardItem(message)
        item.setFont(QtGui.QFont("Consolas", 11))
        item.setForeground(QtGui.QBrush(QtGui.QColor("orange")))
        
        # Устанавливаем флаги, чтобы элемент не был редактируемым и не нажимаемым
        item.setFlags(QtCore.Qt.ItemIsSelectable)  # Только выбор, без редактирования
        
        # Добавляем элемент в модель
        self.model.appendRow(item)
        self.Console.scrollToBottom()

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
