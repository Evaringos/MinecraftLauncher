import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
# ---
from PyQt5.QtCore import QAbstractListModel, Qt
from PyQt5.QtWidgets import QListView, QListWidgetItem

# Добавить возможность переключения темы (AoH Classic; Console92)

# Инициализация иконки
def Icon():
    icon_path = os.path.join(os.path.dirname(__file__), 'cache', 'logo.ico')
    icon = QIcon(icon_path)
    return icon

# Функция для возможности передвижения окна (Используеться только в Stretch в toolbar)
class DraggableStretchWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtCore.Qt.SizeAllCursor)  # Курсор для перетаскивания
        self.setFixedHeight(32)  # Высота должна соответствовать высоте тулбара

        self._drag_start_pos = None
        self._window_pos_at_drag_start = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_pos = event.globalPos()
            self._window_pos_at_drag_start = self.parentWidget().parentWidget().pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._drag_start_pos is not None:
            delta = event.globalPos() - self._drag_start_pos
            new_pos = self._window_pos_at_drag_start + delta
            self.parentWidget().parentWidget().move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_start_pos = None
            self._window_pos_at_drag_start = None
            self.setCursor(QtCore.Qt.SizeAllCursor)

# Launcher MainWindow
class Ui_MainWindow(object):
    # Создание конфига настроек
    def __init__(self):
        self.settings = QtCore.QSettings("AoH Launcher", "Settings")

    # Функция сохранения поля username
    def save_username(self):
        self.settings.setValue("username", self.Username.text())

    def setupUi(self, MainWindow):
        # Отключение дефолтного бара
        # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # MainWindow название и иконка
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("AoH Launcher")
        MainWindow.setWindowIcon(Icon())

        # MainWindow размер и его фиксация
        MainWindow.resize(500, 680)
        MainWindow.setMinimumSize(QtCore.QSize(500, 680))
        MainWindow.setMaximumSize(QtCore.QSize(500, 680))

        # Dark theme
        MainWindow.setStyleSheet("QWidget { background-color: #191919; color: #f2b036; }")

        # Небольшое окно внутри MainWindow для более красивой картинки
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 0, 10, 10) # Высота была 10, но я заменил на 0 для более красивой картинки
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")

        # Toolbar для более удобного использования кнопок
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(self.toolbar)
        self.toolbar.setContentsMargins(0, 0, 0, 0)
        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(32)
        self.toolbar.show()
        # Кнопки внутри тулбара
        # Settings
        self.SettingsButton = QtWidgets.QPushButton("Temp")
        self.SettingsButton.setFixedHeight(32)
        self.SettingsButton.setFixedWidth(32)
        self.toolbar.addWidget(self.SettingsButton)
        # Patch
        self.patchButton = QtWidgets.QPushButton("Патч")
        self.patchButton.setFixedHeight(32)
        self.toolbar.addWidget(self.patchButton)
        # Open Folder
        self.FolderWithGame = QtWidgets.QPushButton("Папка с игрой")
        self.FolderWithGame.setFixedHeight(32)
        self.toolbar.addWidget(self.FolderWithGame)
        # Stratch (Fill the space between buttons)
        stretch_widget = DraggableStretchWidget()
        stretch_layout = QtWidgets.QHBoxLayout(stretch_widget)
        stretch_layout.addStretch(50)
        self.toolbar.addWidget(stretch_widget)
        # Close window
        self.CloseWindow = QtWidgets.QPushButton("Temp")
        self.CloseWindow.setFixedHeight(32)
        self.CloseWindow.setFixedWidth(32)
        self.toolbar.addWidget(self.CloseWindow)
        # Hide Window
        self.HideWindow = QtWidgets.QPushButton("Temp")
        self.HideWindow.setFixedHeight(32)
        self.HideWindow.setFixedWidth(32)
        self.toolbar.addWidget(self.HideWindow)

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
        self.Whattsnew.setMinimumSize(QtCore.QSize(0, 215))
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
        self.Username.setText(self.settings.value("username", ""))
        self.verticalLayout.addWidget(self.Username)
        self.Username.textChanged.connect(self.save_username)
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

        # Поле выбора версии для запуска
        self.VersionName = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VersionName.sizePolicy().hasHeightForWidth())
        self.VersionName.setSizePolicy(sizePolicy)
        self.VersionName.setMinimumSize(QtCore.QSize(100, 35))
        self.VersionName.setObjectName("VersionName")
        self.verticalLayout.addWidget(self.VersionName)
        
        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)

        # Кнопка запуска игры
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