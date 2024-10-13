from PySide6.QtCore import QObject, Signal

class Signals(QObject):
    console_message = Signal(str)
    game_installed = Signal()
    mods_refreshed = Signal()
    play_button_state_changed = Signal(bool, str)

signals = Signals()
