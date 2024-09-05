import tkinter as tk
from tkinter import ttk
import os
import subprocess
import threading
import minecraft_launcher_lib

# Переменная для проверки установки игры
is_game_installed = False

# Переменная для хранения никнейма
username = ""

# Базовая версия игры
base_version = "1.20.1"

# Путь установки игры
minecraft_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')

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
        launch_button.config(state=tk.NORMAL)

# Функция для установки игры
def install_game():
    if is_game_installed:
        print("Игра уже установлена")
        on_installation_complete()
    else:
        progress_bar.start()
        install_thread = threading.Thread(target=install_in_background)
        install_thread.start()

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

# Функция для завершения установки
def on_installation_complete():
    global is_game_installed
    progress_bar.stop()
    is_game_installed = True
    launch_button.config(state=tk.NORMAL)
    print("Игра и Forge установлены")

# Кнопка запуска игры
def launch_game():
    global username
    check_game_installed() # Temp line
    if is_game_installed and forge_version_name:
        username = nickname_entry.get()
        if username:
            print(f"Запуск игры с никнеймом: {username}")
            options = {
                "username": username,
                "uuid": "",
                "token": ""
            }
            # Используем версию Forge для запуска
            command = minecraft_launcher_lib.command.get_minecraft_command(forge_version_name, minecraft_path, options)
            subprocess.call(command)
        else:
            print("Пожалуйста, введите никнейм")

# Кнопка закрытия лаунчера
def show_way():
    os.startfile(minecraft_path)

# Выравнивание позиции открытия окна и размер открываемого окна
def center_window(window, width=300, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Окно и название окна
root = tk.Tk()
root.title("AoH Launcher")

# Установка иконки
icon_path = os.path.join(os.path.dirname(__file__), 'cache', 'logo.ico')
root.iconbitmap(icon_path)

# Центрируем окно
center_window(root)

# Создайте фрейм для выравнивания кнопок
frame = tk.Frame(root)
frame.pack(expand=True, pady=(20, 0))

# Поле для ввода никнейма
nickname_label = tk.Label(frame, text="Введите никнейм:")
nickname_label.pack(pady=5)
nickname_entry = tk.Entry(frame)
nickname_entry.pack(pady=5)

# Кнопка входа в игру
launch_button = tk.Button(frame, text="Играть", command=launch_game, state=tk.DISABLED)
launch_button.pack(pady=10)

# Кнопка начала установки игры
install_button = tk.Button(frame, text="Начать установку", command=install_game)
install_button.pack(pady=10)

# Индикатор прогресса
progress_bar = ttk.Progressbar(frame, mode='indeterminate')
progress_bar.pack(pady=10)

# Кнопка открытия пути проводника
showway_button = tk.Button(frame, text="Открыть папку с игрой", command=show_way)
showway_button.pack(pady=10)

print(f"Путь установки: {minecraft_path}")

# Проверяем, установлена ли игра при запуске лаунчера
check_game_installed()

root.mainloop()