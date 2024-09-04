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

# Версия игры
version = "1.20.1"

# Путь установки игры
minecraft_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')
# minecraft_path = "C:\\Users\\Evarin\\AppData\\Roaming\\AoHLauncher"

# Функция для установки игры
def install_game():
    if os.path.exists(minecraft_path):
        print("Игра уже установлена")
        on_installation_complete()
    else:
        progress_bar.start()
        install_thread = threading.Thread(target=install_in_background)
        install_thread.start()

# Функция для выполнения установки в фоновом режиме
def install_in_background():
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_path)
    root.after(0, on_installation_complete)

# Функция для завершения установки
def on_installation_complete():
    global is_game_installed
    progress_bar.stop()
    is_game_installed = True
    launch_button.config(state=tk.NORMAL)
    print("Игра установлена")

# Кнопка запуска игры
def launch_game():
    global username
    if is_game_installed:
        username = nickname_entry.get()
        if username:
            print(f"Запуск игры с никнеймом: {username}")
            options = {
                "username": username,
                "uuid": "",
                "token": ""
            }
            command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_path, options)
            subprocess.call(command)
        else:
            print("Пожалуйста, введите никнейм")

# Кнопка закрытия лаунчера
def close_window():
    os.startfile(minecraft_path)
    #root.destroy()

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

# Кнопка выхода из лаунчера
close_button = tk.Button(frame, text="Закрыть лаунчер", command=close_window)
close_button.pack(pady=10)

print(f"Путь установки: {minecraft_path}")

root.mainloop()