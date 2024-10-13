import time
import os
import subprocess
import threading
from shutil import rmtree
import minecraft_launcher_lib
from PySide6.QtCore import QObject, Signal
import ConfigHandler
from Signals import signals

# Переменная для проверки установки игры
is_game_installed = False

# Базовая версия игры
base_version = "1.20.1"

# Путь установки игры, модов, конфигов
launcher_path = os.path.expanduser('~/AppData/Roaming/.AoHLauncher')
minecraft_path = os.path.join(launcher_path, 'AoHMinecraft')
aoh_config_file = os.path.join(launcher_path, "AoHConfig.ini")
folder_version = os.path.join(minecraft_path, "versions")
telegram_link = "https://t.me/AspirationOfHolowave"


config = ConfigHandler.read_config()
# Переменная для хранения версии Forge
forge_version_name = None

def DestroyIt():
    signals.console_message.emit("Start the process of deleting minecraft...")
    if os.path.exists(launcher_path):
        if os.path.exists(minecraft_path):
            rmtree(minecraft_path)  # Используем shutil.rmtree для удаления папки рекурсивно
            signals.console_message.emit("Hi from gamelauncher.py!")
            return 1 # all good
        else:
            signals.console_message.emit("Hi from gamelauncher.py!")
            return 0
    else:
        signals.console_message.emit(f"Folder {minecraft_path} isn't exists.")
        signals.console_message.emit("Hi from gamelauncher.py!")
        return 0 # failure

def PlayButtonTextHandler():
    if os.path.exists(folder_version):
        return 1 # ready to play
    else:
        return 0 # neccessary to install the game

# Функция для проверки установки игры при запуске
def check_game_installed():
    global is_game_installed, forge_version_name
    if os.path.exists(folder_version):
        is_game_installed = True
        # Проверяем, установлена ли версия Forge
        versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_path)
        for version in versions:
            if version["id"].startswith(base_version + "-forge"):
                forge_version_name = version["id"]
                break
        signals.play_button_state_changed.emit(True, "Play")

# Есть ли файл конфигурации
def check_configfile():
    if not os.path.exists(launcher_path):
        os.mkdir(launcher_path)
        ConfigHandler.create_default_config()
    elif os.path.exists(launcher_path) and not os.path.exists(aoh_config_file):
        ConfigHandler.create_default_config()

# download zip with minecraft patches.
def CloudDownload():
    signals.console_message.emit("Refreshing mods has been started!")
    start = time.time()
    from CloudDownload import CloudDownload
    CloudDownload("aohminecraft.zip", launcher_path, minecraft_path)
    end = time.time()
    signals.console_message.emit(f"AoH patch is downloaded and extracted in {round(end - start)} s!")
    signals.mods_refreshed.emit()
    
current_max = 100

# Функция для установки игры
def install_game():
#    if is_game_installed:
#        print("Игра уже установлена")
#        on_installation_complete()
#    else:
    install_thread = threading.Thread(target=install_in_background)
    install_thread.start()
    cloud_thread = threading.Thread(target=CloudDownload)
    cloud_thread.start()


# Функция для выполнения установки в фоновом режиме
def install_in_background():
    global forge_version_name
    # Installation callback functions
    def set_status(status: str):
        print(status)

    def set_progress(progress: int): 
        print(f"Progress: {int(progress)}%")  # Print progress as an integer

    def set_max(new_max: int):
        global current_max
        current_max = new_max

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max,
    }

    # Install the base Minecraft version
    minecraft_launcher_lib.install.install_minecraft_version(base_version, minecraft_path, callback=callback)
    
    # Поиск и установка последней доступной версии Forge для указанной версии Minecraft
    # forge_version = minecraft_launcher_lib.forge.find_forge_version(base_version)
    forge_version = "1.20.1-47.3.10"
    if forge_version:
        forge_version_name = minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_path)
        signals.console_message.emit("Forge has been installed")
        
        # на этой строчке зависает
        global is_game_installed
        is_game_installed = True
        signals.play_button_state_changed.emit(True, "Play")
        check_game_installed()
    else:
        signals.console_message.emit("Can't find forge version for Minecraft")

# Скачивание модов и конфига

# Кнопка запуска игры
def launch_game(username):
    # check_game_installed() # Temp line
    if is_game_installed and forge_version_name:
        config = ConfigHandler.read_config()
        if username:
            options = {
                "username": username,
                "jvmArguments": [f"-Xmx{config['Launcher']['ram']}G","-Xms3G"],
            }
            signals.console_message.emit(f"Launching game with username: {username}")
            # Используем версию Forge для запуска
            command = minecraft_launcher_lib.command.get_minecraft_command\
                (forge_version_name, minecraft_path, options)
            subprocess.call(command, creationflags=0x08000000) #CREATE_NO_WINDOW
        else:
            signals.console_message.emit("Can't launch the game without username!")


signals.console_message.emit(f"Installing path: {minecraft_path}")

# Проверяем, установлена ли игра при запуске лаунчера
check_game_installed()
check_configfile() # есть ли конфиг
