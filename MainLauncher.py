import sys, os, threading
from ctypes import WinDLL
from ctypes.wintypes import MSG
import win32con, win32gui, win32api
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtCore import Qt, QAbstractListModel, QAbstractNativeEventFilter, QByteArray
from PySide6.QtCore import QModelIndex, QUrl, QObject, Slot, Signal, Property
from Signals import signals
import GameLauncher


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

    def appendText(self, text):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._texts.append(text)
        self.endInsertRows()

class PlayButtonBridge(QObject):
    play_button_text_changed = Signal(str)
    button_enabled_chanded = Signal(bool)
    def __init__(self):
        super().__init__()
        self._play_button_text = "Error"
        self._button_enabled = True
        signals.play_button_state_changed.connect(self.set_button_enabled)
        signals.play_button_text_changed.connect(self.set_play_button_text)
        GameLauncher.check_game_installed()

    def get_play_button_text(self) -> str :
        return self._play_button_text

    def get_button_enabled(self) -> bool :
        return self._button_enabled

    
    def set_play_button_text(self, text: str):
        if self._play_button_text != text:
            self._play_button_text = text
            self.play_button_text_changed.emit(text)
            # signals.play_button_text_changed.emit(text)

    def set_button_enabled(self, enabled: bool):
        if self._button_enabled != enabled:
            self._button_enabled = enabled
            self.button_enabled_chanded.emit(enabled)
            # signals.play_button_state_changed.emit(enabled)

    play_button_text = Property(str, get_play_button_text, set_play_button_text,
                                notify=play_button_text_changed)
    button_enabled = Property(bool, get_button_enabled, set_button_enabled,
                              notify=button_enabled_chanded)


    @Slot()
    def play_pressed(self):
        if os.path.exists(GameLauncher.version_folder):
            signals.console_message.emit("Starting to launch the game!")
            signals.console_message.emit(f"game installed: {GameLauncher.is_game_installed}")
            signals.console_message.emit(f"forge: {GameLauncher.forge_version_name}")
            GameLauncher.launch_game("Stradlater")
        else:
            signals.console_message.emit("Starting downloading the game!")
            signals.console_message.emit("Please don't close this window!")
            signals.play_button_state_changed.emit(False) # dont chane title
            signals.play_button_text_changed.emit("Installing")
            GameLauncher.install_game()

class UsernameInputHandler(QObject):
    username_changed = Signal(str)
    def __init__(self):
        super().__init__()
        self.username = "Steve"
        signals.username_changed.connect(self.set_username)
        GameLauncher.Username.usernameFromConfig()
        

    def set_username(self, username:str):
        if self.username != username:
            self.username = username
            GameLauncher.Username.usernameToConfig(username)
            signals.username_changed.emit(username)

    def get_username(self) -> str :
        return self.username

    username_text = Property(str, get_username, set_username,
                             notify=username_changed)
    
    # @Slot(str)
    # def inputUsername(self, username):
        # self.username = username

class ToolBarButtonHandler(QObject):
    @Slot()
    def deleteMinecraft(self):
        GameLauncher.DeleteMinecraft()        
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

        
class Bridge(QObject):
    @Slot(QObject)
    def setFlags(self, window):
        self.window = window
        hwnd = int(self.window.winId())
        self.event_filter = WinEventFilter()
        QApplication.instance().installNativeEventFilter(self.event_filter)
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE,# | 
                       win32con.WS_POPUP		# ||
                       | win32con.WS_SYSMENU		# ||| setting style to restore show-hide animations
                       | win32con.WS_CAPTION		# ||
                       | win32con.WS_MINIMIZEBOX)	# |
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style |= win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,style)
        transparent_color = win32api.RGB(0,0,0)
        hdc = win32gui.GetDC(hwnd)
        win32gui.SetBkColor(hdc, transparent_color)
        win32gui.ReleaseDC(hwnd, hdc)


        

    # to bring back close animation
    @Slot(QObject)
    def aboutToClose(self, window):
        self.window = window
        hwnd = int(self.window.winId())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style &= ~win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,style)
        self.window.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("cache/aoh_icon.ico"))
    engine = QQmlApplicationEngine()
    bridge = Bridge()
    toolbar_button_handler = ToolBarButtonHandler()
    play_button_handler = PlayButtonBridge()
    console_model = ConsoleModel()
    username_handler = UsernameInputHandler()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("toolbarButtonHandler", toolbar_button_handler)
    engine.rootContext().setContextProperty("playButton", play_button_handler)
    engine.rootContext().setContextProperty("username", username_handler)
    engine.rootContext().setContextProperty("consoleModel", console_model)
    engine.load(QUrl("qml/app.qml"))
    if not engine.rootObjects(): sys.exit(-1)
    sys.exit(app.exec())

# Изменить scroll bar у Console
# DONE доавить визуал на фон лаунчера
# Выровнять Play по центру
