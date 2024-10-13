import sys, os, threading
from ctypes import byref, WinDLL
from ctypes.wintypes import RECT, MSG
import win32con, win32gui
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import Qt, QAbstractListModel, QAbstractNativeEventFilter, QByteArray, QModelIndex, QUrl, QObject, Slot, Signal, Property
import GameLauncher
from Signals import signals
        

dwmapi = WinDLL("dwmapi.dll")
user32 = WinDLL("user32.dll")

class WinEventFilter(QAbstractNativeEventFilter):
    def nativeEventFilter(self, eventType, message):
        if eventType == QByteArray(b"windows_generic_MSG"):
            msg = MSG.from_address(message.__int__())
            # This whole bullshit was made for only preventing Windows to draw vanilla titlebar
            if msg.message == win32con.WM_NCCALCSIZE:
                return True, 0
        return False, 0

class ConsoleModel(QAbstractListModel):
    TextRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._texts = []
        signals.console_message.connect(self.appendText)

    def rowCount(self, parent=QModelIndex()):
        return len(self._texts)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if 0 <= index.row() < len(self._texts):
            if role == ConsoleModel.TextRole:
                return self._texts[index.row()]
        return None

    def roleNames(self):
        return {ConsoleModel.TextRole: b'text'}

    @Slot(str)
    def appendText(self, text):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._texts.append(text)
        self.endInsertRows()

class PlayButtonTextBridge(QObject):
    PlayButtonState = Signal()
    PlayButtonText = Signal()
    
    def __init__(self):
        super().__init__()
        self._play_button_text = "Error"
        self._button_enabled = True
        signals.play_button_state_changed.connect(self.update_button_state)

    @Property(str, notify=signals.play_button_state_changed)
    def play_button_text(self):
        return self._play_button_text

    @Property(bool, notify=signals.play_button_state_changed)
    def button_enabled(self):
        return self._button_enabled
       
    @Slot(bool, str)
    def update_button_state(self, enabled:bool, text:str):
        self._button_enabled = enabled
        self._play_button_text = text
        signals.play_button_state_changed.emit(enabled, text)

    @Slot()
    def play_pressed(self):
        result = GameLauncher.PlayButtonTextHandler()
        match result:
            case 1: # ready to play
                signals.console_message.emit("Starting to launch the game!")
                signals.console_message.emit(f"game installed: {GameLauncher.is_game_installed}")
                signals.console_message.emit(f"forge: {GameLauncher.forge_version_name}")
                GameLauncher.launch_game("Stradlater")
            case 0: # need in downloading the game
                signals.console_message.emit("Starting downloading the game!")
                signals.console_message.emit("Please don't close this window!")
                signals.play_button_state_changed.emit(False, self._play_button_text)
                GameLauncher.install_game()
        

class Bridge(QObject):
    @Slot()
    def deleteMinecraft(self):
        result = GameLauncher.DestroyIt()
        match result:
            case 1:
                signals.console_message.emit(f"Folder {GameLauncher.minecraft_path} has been sucess deleted.")
            case 0:
                signals.console_message.emit(f"Folder {GameLauncher.minecraft_path} isn't exists")
            case _:
                print("Невозможно")
    
    @Slot()	# on open game location pressed
    def open_folder(self):
        if (os.path.exists(GameLauncher.launcher_path) & os.path.exists(GameLauncher.minecraft_path)):
            QDesktopServices.openUrl(QUrl.fromLocalFile(GameLauncher.minecraft_path))
        else: signals.console_message.emit("The game is not installed yet.")

    @Slot()	# on refresh button pressed
    def refreshClicked(self):
        CloudThread = threading.Thread(target=GameLauncher.CloudDownload)
        CloudThread.start()
    
    @Slot()	# on open discord pressed
    def openTelegram(self):
        QDesktopServices.openUrl(QUrl(GameLauncher.telegram_link))
        

    @Slot()
    def credits(self):
        signals.console_message.emit("---================---")
        signals.console_message.emit("CEO of project - Scavenger (Evaringos)")
        signals.console_message.emit("Core programmer - Stradlater25")
        signals.console_message.emit("Designer / Community manager - Xeenomiya")
        signals.console_message.emit("---================---")

    @Slot(QObject)
    def setFlags(self, window):
        self.window = window
        hwnd = int(self.window.winId())
        self.event_filter = WinEventFilter()
        QApplication.instance().installNativeEventFilter(self.event_filter)
        win32gui.SetWindowLong(hwnd, -16,		# | 
                       win32con.WS_POPUP		# ||
                       | win32con.WS_SYSMENU		# ||| setting style to restore show-hide animations
                       | win32con.WS_CAPTION		# ||
                       | win32con.WS_MINIMIZEBOX)	# |
        margins = RECT(-1, -1, -1, -1)					# | setting shadow
        dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))	# |

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("cache/aoh_icon.ico"))
    bridge = Bridge()
    playButton = PlayButtonTextBridge()
    engine = QQmlApplicationEngine()
    console_model = ConsoleModel()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("playButton", playButton)
    engine.rootContext().setContextProperty("consoleModel", console_model)
    engine.load(QUrl("qml/app.qml"))
    if not engine.rootObjects(): sys.exit(-1)
    sys.exit(app.exec())

# Изменить scroll bar у Console
# DONE доавить визуал на фон лаунчера
# Выровнять Play по центру
