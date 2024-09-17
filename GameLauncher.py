import os
import subprocess
import threading
import minecraft_launcher_lib
from webdav3.client import Client
from ConfigHandler import create_default_config
import secret


# Переменная для проверки установки игры
is_game_installed = False

# Базовая версия игры
base_version = "1.20.1"

# Путь установки игры, модов, конфигов
minecraft_path = os.path.expanduser('~/AppData/Roaming/.AoHLauncher')
aoh_config_file = os.path.join(minecraft_path, "AoHConfig.ini")
# Переменная для хранения версии Forge
forge_version_name = None

# Функция для проверки установки игры при запуске
def check_game_installed():
    global is_game_installed, forge_version_name
    if os.path.exists(minecraft_path):
        print("Игра уже установлена")
        is_game_installed = True
        # Проверяем, установлена ли версия Forge
        versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_path)
        for version in versions:
            if version["id"].startswith(base_version + "-forge"):
                forge_version_name = version["id"]
                break

# Есть ли файл конфигурации
def check_configfile():
    if not os.path.isfile(aoh_config_file): create_default_config()

# Функция для установки игры
def install_game():
    if is_game_installed:
        print("Игра уже установлена")
        on_installation_complete()
    else:
        install_thread = threading.Thread(target=install_in_background)
        install_thread.start()
        cloudDownload()

# Функция для выполнения установки в фоновом режиме
def install_in_background():
    global forge_version_name
    # Установка базовой версии Minecraft
    minecraft_launcher_lib.install.install_minecraft_version(base_version, minecraft_path)
    
    # Поиск и установка последней доступной версии Forge для указанной версии Minecraft
    forge_version = minecraft_launcher_lib.forge.find_forge_version(base_version)
    if forge_version:
        forge_version_name = minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_path)
        print("Forge установлен")
    else:
        print("Forge версия не найдена для данной версии Minecraft")
    
    root.after(0, on_installation_complete)



# Скачивание модов и конфига
def cloudDownload (): # ЭТА КЭЭМЕЛ КЕЙС
    options = { 'webdav_hostname' : secret.davlink,
                'webdav_login' : secret.davlogin,
                'webdav_password' : secret.davpass,
                'disable_check': True } #иначе ломается
    client = Client(options)
    client.download("minecraft/config", os.path.join(minecraft_path, "config"))
    client.download("minecraft/mods", os.path.join(minecraft_path, "mods"))

    
# Функция для завершения установки
def on_installation_complete():
    global is_game_installed
    is_game_installed = True
    print("Игра и Forge установлены")

# Кнопка запуска игры
def launch_game(username):
    # check_game_installed() # Temp line
    if is_game_installed and forge_version_name:
        if username:
            print(f"Запуск игры с никнеймом: {username}")
            # Используем версию Forge для запуска
            command = minecraft_launcher_lib.command.get_minecraft_command\
                (forge_version_name, minecraft_path, {"username": username})
            CREATE_NO_WINDOW = 0x08000000
            subprocess.call(command, creationflags=CREATE_NO_WINDOW)
        else:
            print("Пожалуйста, введите никнейм")


print(f"Путь установки: {minecraft_path}")

# Проверяем, установлена ли игра при запуске лаунчера
check_game_installed()
check_configfile()

