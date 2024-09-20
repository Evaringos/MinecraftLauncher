import os
import subprocess
import threading
import minecraft_launcher_lib
from PyQt5.QtCore import QObject, pyqtSignal
from webdav3.client import Client
from ConfigHandler import create_default_config
import secret


# Переменная для проверки установки игры
is_game_installed = False

# Базовая версия игры
base_version = "1.20.1"

DownloadCompleted = False

# Путь установки игры, модов, конфигов
minecraft_path = os.path.expanduser('~\\AppData\\Roaming\\.AoHLauncher')
aoh_config_file = os.path.join(minecraft_path, "AoHConfig.ini")
folder_version = os.path.join(minecraft_path, "versions")
# Переменная для хранения версии Forge
forge_version_name = None

class ConsoleMessageClass(QObject):
    message_signal = pyqtSignal(str)
    
    def Send (self, message):
        self.message_signal.emit(message)
        
ConsoleMessage = ConsoleMessageClass() # создаю экземпляр чтобы можно было потом выгрузить его в Main
def GetConsoleMessage():
    return ConsoleMessage

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

# Есть ли файл конфигурации
def check_configfile():
    if not os.path.exists(minecraft_path): 
        os.mkdir(minecraft_path)
        create_default_config()


#    if not os.path.isfile(aoh_config_file): create_default_config()

# Функция для установки игры
def install_game():
#    if is_game_installed:
#        print("Игра уже установлена")
#        on_installation_complete()
#    else:
    install_thread = threading.Thread(target=install_in_background)
    install_thread.start()
#        cloudDownload()

# Функция для выполнения установки в фоновом режиме
def install_in_background():
    global forge_version_name
    # Установка базовой версии Minecraft
    minecraft_launcher_lib.install.install_minecraft_version(base_version, minecraft_path)
    
    # Поиск и установка последней доступной версии Forge для указанной версии Minecraft
    forge_version = minecraft_launcher_lib.forge.find_forge_version(base_version)
    if forge_version:
        forge_version_name = minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_path)
        cloudDownload() # Добавил еще раз эту функцию здесь, так как в MainLauncher не работало
        DownloadCompleted = True
        ConsoleMessage.Send("Forge установлен")
        on_installation_complete()
        return DownloadCompleted
    else:
        ConsoleMessage.Send("Forge версия не найдена для данной версии Minecraft")
    
    # root.after(0, on_installation_complete)
    # root.after(0, on_installation_complete) # Строчка вызывает ошибку



# Скачивание модов и конфига
def cloudDownload (): # ЭТА КЭЭМЕЛ КЕЙС
    options = { 'webdav_hostname' : secret.davlink,
                'webdav_login' : secret.davlogin,
                'webdav_password' : secret.davpass,
                'disable_check': True } #иначе ломается
    client = Client(options)
    client.download_file("minecraft/options.txt", os.path.join(minecraft_path, "options.txt"))
    client.download("minecraft/config", os.path.join(minecraft_path, "config"))
    client.download("minecraft/mods", os.path.join(minecraft_path, "mods"))
    
    
# Функция для завершения установки
def on_installation_complete():
    global is_game_installed
    is_game_installed = True
    ConsoleMessage.Send("Игра и Forge установлены")

# Кнопка запуска игры
def launch_game(username):
    # check_game_installed() # Temp line
    if is_game_installed and forge_version_name:
        if username:
            ConsoleMessage.Send(f"Запуск игры с никнеймом: {username}")
            # Используем версию Forge для запуска
            command = minecraft_launcher_lib.command.get_minecraft_command\
                (forge_version_name, minecraft_path, {"username": username})
            CREATE_NO_WINDOW = 0x08000000
            subprocess.call(command, creationflags=CREATE_NO_WINDOW)
        else:
            ConsoleMessage.Send("Пожалуйста, введите никнейм")


ConsoleMessage.Send(f"Путь установки: {minecraft_path}")

# Проверяем, установлена ли игра при запуске лаунчера
check_game_installed()
check_configfile()
