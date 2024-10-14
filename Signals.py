from PySide6.QtCore import QObject, Signal

class Signals(QObject):
    console_message = Signal(str)
    game_installed = Signal()
    mods_refreshed = Signal()
    play_button_state_changed = Signal(bool)
    play_button_text_changed = Signal(str)
    username_changed = Signal(str)

signals = Signals()
