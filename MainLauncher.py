import sys, os
import GameLauncher
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QColor, QIcon, QDesktopServices, QPainter, QPalette, QPixmap
from PyQt5.QtCore import QPoint, QUrl, QSize, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgRenderer
from ConfigHandler import update_config, read_config, create_default_config
from Themes import Theme
import GameFolderDestroyer

config = GameLauncher.config

class Ui_MainWindow(QtWidgets.QMainWindow):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Проверяем, находится ли курсор над тулбаром
            toolbar_pos = self.toolbar.mapToGlobal(self.toolbar.rect().topLeft())
            toolbar_rect = self.toolbar.rect()
            toolbar_rect.moveTo(toolbar_pos)
            if toolbar_rect.contains(event.globalPos()):
                self.dragging = True
                self.offset = event.globalPos() - self.pos()
        
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def refresh_icons (self):
        self.SettingsButton.setIcon(QIcon(Theme.Icon.SVGIcon("settings")))
        self.FolderWithGame.setIcon(QIcon(Theme.Icon.SVGIcon("folder")))
        self.Refresh.setIcon(QIcon(Theme.Icon.SVGIcon("reload")))
        self.HideWindow.setIcon(QIcon(Theme.Icon.SVGIcon("hide")))
        self.CloseWindow.setIcon(QIcon(Theme.Icon.SVGIcon("close")))
        self.Credits.setIcon(QIcon(Theme.Icon.SVGIcon("info")))
        self.language_menu.setIcon(QIcon(Theme.Icon.SVGIcon("globe")))
        self.theme_menu.setIcon(QIcon(Theme.Icon.SVGIcon("brush")))
        self.Delete.setIcon(QIcon(Theme.Icon.SVGIcon("bin")))
        self.DiscordButton.setIcon(QIcon(Theme.Icon.SVGIcon("discord")))
        self.RamSelected.setIcon(QIcon(Theme.Icon.SVGIcon("memory")))
        
    def update_theme(self, theme=None):
        if theme : # if func called with theme argument
            Theme.SetTheme(self, theme)
            update_config("Launcher", "theme", theme)
            self.refresh_icons()
        else: #if just update_theme()
            if config["Launcher"]["theme"]:
                Theme.SetTheme(self, config["Launcher"]["theme"])
                self.refresh_icons()
            #if there's no theme in config
            if not config["Launcher"]["theme"]:
                self.Console.addItem("There's no theme in config. Setting AoHClassic theme")
                update_config("Launcher", "theme", "AoHClassic")
                Theme.SetTheme(self, config["Launcher"]["theme"])
                self.refresh_icons()
    
    def RamChanged(self, ram):
        update_config("Launcher", "ram", ram)
    
    def LanguageChanged(self, language=None):
        if language :
            update_config("Launcher", "language", language)
        # self.Console.addItem("There's no others languages yet!")
        # print("There's no others languages yet!")

    # Button handler
    def PlayButtonPressed(self):
        if not os.path.exists(GameLauncher.folder_version):
            self.InstallingProcess()
            self.Console.addItem("Starting of downloading game!")
            self.Console.addItem("Please do not close this window!")
            self.PlayButton.setEnabled(False) 
            self.SettingsButton.setEnabled(False)
            self.Refresh.setEnabled(False)
            self.progressBar.setVisible(True)
            GameLauncher.install_game()
        elif os.path.exists(GameLauncher.folder_version):
            self.hide()
            GameLauncher.launch_game(self.Username.text())
            self.show()
            self.Console.addItem("Play session has been ended!")
        else:
            self.Console.addItem("Unknown command!")
    
    def RefreshClicked(self):
        self.InstallingProcess()
        self.progressBar.setVisible(True)
        self.Refresh.setEnabled(False)
        self.SettingsButton.setEnabled(False)
        self.PlayButton.setEnabled(False)
        CloudThread = threading.Thread(target=GameLauncher.CloudDownload)
        CloudThread.start()

    # Button statement update
    def ButtonTextChange(self): 
        if os.path.exists(GameLauncher.folder_version):
            self.PlayButton.setText("Play")
        else:
            self.PlayButton.setText("Install game")

    # Insalling text functions:
    def InstallingProcess(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.UpdateInstallingText)
        self.timer.start(500)  # 500 milliseconds = 0.5 seconds

    def InstallationComplete(self):
        self.timer.stop()  # Timer stops when installing is done
        self.ButtonTextChange()

    def UpdateInstallingText(self):
        texts = ["Installing.  ", "Installing.. ", "Installing..."]
        current_text = self.PlayButton.text()
        if current_text in texts:
            index = texts.index(current_text)
            next_index = (index + 1) % len(texts)
            self.PlayButton.setText(texts[next_index])
        else:
            self.PlayButton.setText(texts[0])
    
    def GameInstallingDone(self):
        self.PlayButton.setText("Play")
        self.PlayButton.setEnabled(True)
        self.SettingsButton.setEnabled(True)
        self.Refresh.setEnabled(True)
        self.progressBar.setVisible(False)
        self.Console.addItem("The game is ready to launch!")

    def save_username_and_exit(self):
        update_config("Launcher", "Username", self.Username.text())
        # Починить закрытие майнкрафта
        self.close()


    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("AoH Launcher", "Settings")
        self.game_installed = GameLauncher.GetGameInstalled()  # Создаем экземпляр класса GameInstalled
        self.mods_refreshed = GameLauncher.GetModsRefreshed()
        self.game_installed.installed_signal.connect(self.GameInstallingDone)
        self.game_installed.installed_signal.connect(self.InstallationComplete)
        self.mods_refreshed.refresh_signal.connect(self.GameInstallingDone)
        self.mods_refreshed.refresh_signal.connect(self.InstallationComplete)

        app.setWindowIcon(QtGui.QIcon('cache/aoh_icon.ico'))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) # отключение рамки окна
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.dragging = False
        # self.offset = QPoint()        



        self.setObjectName("MainWindow")
        self.setWindowTitle("AoH Launcher")
        self.setMinimumSize(QtCore.QSize(500, 595))
        self.setMaximumSize(QtCore.QSize(500, 595))

        self.centrallayout = QtWidgets.QWidget()
        self.horizontalLayout = QtWidgets.QHBoxLayout() # used in toolbar
        self.setCentralWidget(self.centrallayout)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centrallayout)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setSpacing(5)
        
        # Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setObjectName("Toolbar")
        self.verticalLayout.addWidget(self.toolbar)
        # self.toolbar.setContentsMargins(0, 0, 0, 0)
        self.toolbar.setMovable(False)
        
        self.toolbar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu) # Отключение встроенной функции удаления тулбара
        

        game_folder_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')

        # Настройка кнопки Settings
        self.SettingsButton = QtWidgets.QPushButton()
        self.SettingsButton.setObjectName("SettingsButton")
        self.SettingsButton.setProperty("iconprop", True)
        self.toolbar.addWidget(self.SettingsButton)

        
        # Создаем выпадающее меню (dropdown menu)
        self.settings_menu = QtWidgets.QMenu(self.centrallayout)
        self.theme_menu = QtWidgets.QMenu("Themes settings", self.settings_menu)
        self.language_menu = QtWidgets.QMenu("Language settings", self.settings_menu)
        self.RamSelected = QtWidgets.QMenu("Number of RAM", self.settings_menu)
        self.Credits = QtWidgets.QAction("Credits", self.settings_menu)
        self.Delete = QtWidgets.QAction("Delete Minecraft", self.settings_menu)

        # Создаём группы действий
        self.theme_menu_group = QtWidgets.QActionGroup(self)
        self.theme_menu_group.setExclusive(True)

        self.ram_menu_group = QtWidgets.QActionGroup(self)
        self.ram_menu_group.setExclusive(True)

        self.language_menu_group = QtWidgets.QActionGroup(self)
        self.language_menu_group.setExclusive(True)
        
        # Создаем действия для меню
        self.theme_option1 = self.theme_menu_group.addAction("AoH Classic")
        self.theme_option2 = self.theme_menu_group.addAction("Console92")
        self.theme_option3 = self.theme_menu_group.addAction("GruvBox")
        self.theme_option4 = self.theme_menu_group.addAction("Green Hill")

        self.theme_menu.addAction(self.theme_option1)
        self.theme_menu.addAction(self.theme_option2)   
        self.theme_menu.addAction(self.theme_option3)
        self.theme_menu.addAction(self.theme_option4)     

        self.theme_option1.setCheckable(True)
        self.theme_option2.setCheckable(True)
        self.theme_option3.setCheckable(True)
        self.theme_option4.setCheckable(True)
        if config["Launcher"]["Theme"] == "AoHClassic": self.theme_option1.setChecked(True) #Галочка по дефолту
        elif config["Launcher"]["Theme"] == "Console92": self.theme_option2.setChecked(True)
        elif config["Launcher"]["Theme"] == "GruvBox": self.theme_option3.setChecked(True)
        elif config["Launcher"]["Theme"] == "Green Hill": self.theme_option4.setChecked(True)

        self.RamOption1 = self.ram_menu_group.addAction("2 Gb")
        self.RamOption2 = self.ram_menu_group.addAction("4 Gb")
        self.RamOption3 = self.ram_menu_group.addAction("8 Gb")
        self.RamOption4 = self.ram_menu_group.addAction("12 Gb")
        self.RamOption5 = self.ram_menu_group.addAction("18 Gb")

        self.RamSelected.addAction(self.RamOption1)
        self.RamSelected.addAction(self.RamOption2)
        self.RamSelected.addAction(self.RamOption3)
        self.RamSelected.addAction(self.RamOption4)
        self.RamSelected.addAction(self.RamOption5)

        self.RamOption1.setCheckable(True)
        self.RamOption2.setCheckable(True)
        self.RamOption3.setCheckable(True)
        self.RamOption4.setCheckable(True)
        self.RamOption5.setCheckable(True)
        if config["Launcher"]["ram"] == "8": self.RamOption3.setChecked(True)
        elif config["Launcher"]["ram"] == "2": self.RamOption1.setChecked(True)
        elif config["Launcher"]["ram"] == "4": self.RamOption2.setChecked(True)
        elif config["Launcher"]["ram"] == "12": self.RamOption4.setChecked(True)
        elif config["Launcher"]["ram"] == "18": self.RamOption5.setChecked(True)

        self.language_option1 = self.language_menu_group.addAction("English")
        self.language_option2 = self.language_menu_group.addAction("Русский")

        self.language_menu.addAction(self.language_option1)
        self.language_menu.addAction(self.language_option2)

        self.language_option1.setCheckable(True)
        self.language_option2.setCheckable(True)
        if config["Launcher"]["language"] == "eng": self.language_option1.setChecked(True)
        elif config["Launcher"]["language"] == "rus": self.language_option2.setChecked(True)
        
        # Подключаем слоты для действий. triggered - действие только когда галка ставится
        self.theme_option1.triggered.connect(lambda: self.update_theme("AoHClassic"))
        self.theme_option2.triggered.connect(lambda: self.update_theme("Console92"))
        self.theme_option3.triggered.connect(lambda: self.update_theme("GruvBox"))
        self.theme_option4.triggered.connect(lambda: self.update_theme("Green Hill"))
        self.language_option1.toggled.connect(lambda: self.LanguageChanged("eng"))
        self.language_option2.toggled.connect(lambda: self.LanguageChanged("rus"))
        self.RamOption1.toggled.connect(lambda: self.RamChanged("2"))
        self.RamOption2.toggled.connect(lambda: self.RamChanged("4"))
        self.RamOption3.toggled.connect(lambda: self.RamChanged("8"))
        self.RamOption4.toggled.connect(lambda: self.RamChanged("12"))
        self.RamOption5.toggled.connect(lambda: self.RamChanged("18"))
        self.Credits.triggered.connect(lambda: ShowCredits())
        self.Delete.triggered.connect(lambda: DeleteMinecraft())
        
        # Добавляем вложенное меню в основное меню
        self.settings_menu.addMenu(self.theme_menu)
        self.settings_menu.addMenu(self.language_menu)
        self.settings_menu.addMenu(self.RamSelected)
        self.settings_menu.addAction(self.Credits)
        self.settings_menu.addAction(self.Delete)
        self.SettingsButton.setMenu(self.settings_menu) # Привязываем меню к кнопке
        self.SettingsButton.setToolTip("Settings")

        # Папка с игрой
        self.FolderWithGame = QtWidgets.QPushButton()
        self.FolderWithGame.setToolTip("Open folder with game")
        self.FolderWithGame.setProperty("iconprop", True)
        self.toolbar.addWidget(self.FolderWithGame)

        
        # Метод для открытия папки
        def open_folder():
            if os.path.exists(GameLauncher.launcher_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(game_folder_path))
            else:
                self.Console.addItem("The game is not installed yet")
        # Подключение метода к нажатию кнопки
        self.FolderWithGame.clicked.connect(open_folder)

        # Ссылка на сервер проекта
        self.DiscordButton = QtWidgets.QPushButton()
        self.DiscordButton.setToolTip("Our discord!")
        self.DiscordButton.setProperty("iconprop", True)
        self.toolbar.addWidget(self.DiscordButton)

        # Метод для открытия ссылки
        def OpenDiscord():
            url = QUrl("https://discord.gg/DTHu4rZjmM")
            QDesktopServices.openUrl(url)
        # Подключение метода к нажатию кнопки
        self.DiscordButton.clicked.connect(OpenDiscord)

        # Обновление модов (возможно временная функция)
        self.Refresh = QtWidgets.QPushButton()
        self.Refresh.setToolTip("Reinstall mods")
        self.Refresh.setProperty("iconprop", True)
        self.toolbar.addWidget(self.Refresh)

        # def refresh_mods():
        self.Refresh.clicked.connect(self.RefreshClicked)

        # Stretch
        self.Stretch = QtWidgets.QWidget()
        self.Stretch.setObjectName("Stretch")
        self.Stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.toolbar.addWidget(self.Stretch)
        
        # Hide window button
        self.HideWindow = QtWidgets.QPushButton(self.centrallayout)
        self.HideWindow.setProperty("iconprop", True)
        self.HideWindow.setToolTip("Hide")
        self.HideWindow.clicked.connect(self.showMinimized)
        self.toolbar.addWidget(self.HideWindow)
        
        # Close window button
        self.CloseWindow = QtWidgets.QPushButton()
        self.CloseWindow.setProperty("iconprop", True)
        self.CloseWindow.setToolTip("Close")        
        self.CloseWindow.clicked.connect(self.save_username_and_exit)
        self.toolbar.addWidget(self.CloseWindow)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        # Консоль для более отзывчивого интерфейса
        self.Console = QtWidgets.QListWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.Console.setSizePolicy(sizePolicy)
        self.Console.setMinimumSize(QtCore.QSize(0, 210))
        self.Console.setObjectName("Console")
        self.verticalLayout.addWidget(self.Console)
        self.ConsoleSlot = GameLauncher.GetConsoleMessage()
        self.ConsoleSlot2 = GameFolderDestroyer.GetConsoleMessage()
        self.ConsoleSlot.message_signal.connect(self.Console.addItem)
        self.ConsoleSlot2.message_signal.connect(self.Console.addItem)
        self.Console.addItem("Launcher started")
        

        # Spacer
        spacerItem1 = QtWidgets.QSpacerItem(100, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)

        # Поле ввода Username
        self.Username = QtWidgets.QLineEdit()
        self.Username.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.Username.setSizePolicy(sizePolicy)
        self.Username.setMinimumSize(QtCore.QSize(100, 35))
        self.Username.setDragEnabled(False)
        self.Username.setReadOnly(False)
        self.Username.setClearButtonEnabled(False)
        self.Username.setText(config["Launcher"]["Username"])
        self.verticalLayout.addWidget(self.Username)        

        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        # Кнопка запуска игры Play button
        self.PlayButton = QtWidgets.QPushButton()
        self.PlayButton.setMinimumSize(QtCore.QSize(150, 40))
        self.PlayButton.setObjectName("PlayButton")
        self.ButtonTextChange()
        self.PlayButton.clicked.connect(self.PlayButtonPressed)
        self.verticalLayout.addWidget(self.PlayButton)
        # self.PlayButton.clicked.connect(self.launch_game_pressed)

        # Progressbar внутри кнопки play
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setVisible(False)  # Видимость прогресс-бара
        self.progressBar.setTextVisible(False)
        effect = QGraphicsOpacityEffect(self.progressBar)
        effect.setOpacity(0.3)
        self.progressBar.setGraphicsEffect(effect)
        self.progressBar.setValue(100)

        # Добавляем прогресс-бар к кнопке
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.progressBar)
        self.PlayButton.setLayout(layout)
              
        #Tail
        self.update_theme()
        # self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


        def ShowCredits():
            self.Console.addItem("---================---")
            self.Console.addItem("CEO of project - Scavenger (Evaringos)")
            self.Console.addItem("Core programmer - Stradlater25")
            self.Console.addItem("Designer / Community manager - Xeenomiya")
            self.Console.addItem("---================---")
        
        def DeleteMinecraft():
            GameFolderDestroyer.MinecraftDestroyer.DestroyIt()
            self.ButtonTextChange()

        
        # Launcher Translate
        # def retranslateUi():
            # _translate = QtCore.QCoreApplication.translate
            # self.Username.setPlaceholderText(_translate("MainWindow", "Username:"))
            # self.patchButton.setText(_translate("MainWindow", "patchButton"))
            # self.FolderWithGame.setText(_translate("MainWindow", "folderButton"))
            # self.PlayButton.setText(_translate("MainWindow", "Play"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

# Изменить scroll bar у Console
# Добавить визуал на фон лаунчера
# Выровнять Play по центру
