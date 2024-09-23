import os
from PyQt5 import QtWidgets, QtCore
import re

from GameLauncher import ConsoleMessage

class IconManager:
    def __init__(self):
        self.temp_files = {}  # Словарь для хранения временных файлов
        self.icons = {
            'settings': 'cache/icons/cogwheel.svg',
            'hide': 'cache/icons/hide.svg',
            'close': 'cache/icons/close.svg',
            'folder': 'cache/icons/folder.svg',
            'globe': 'cache/icons/globe.svg',
            'brush': 'cache/icons/brush.svg',
            'reload': 'cache/icons/reload.svg',
            'info': 'cache/icons/info.svg',
            'bin': 'cache/icons/bin.svg',
            'discord': 'cache/icons/discord.svg',
        }

    def ColorizeIcon(self, iconname: str, color: str):
        with open(self.icons[iconname], 'r') as file:
            svg_content = file.read()
        svg_content = re.sub(r'fill="[^"]+"', f'fill="{color}"', svg_content)
        # Создаем уникальный ключ для иконки
        key = f"{iconname}_{color}"
        # Если для этой иконки уже есть временный файл, используем его
        if key in self.temp_files:
            return self.temp_files[key].fileName()
        # Иначе создаем новый временный файл
        temp_file = QtCore.QTemporaryFile()
        temp_file.open()
        temp_file.write(svg_content.encode())
        temp_file.close()
        self.temp_files[key] = temp_file # Сохраняем временный файл в словаре
        return temp_file.fileName()

    def SVGIcon(self, iconname):
        return (self.ColorizeIcon(iconname, Theme.IconColor))


    
class Theme(QtWidgets.QMainWindow):
    IconColor = '#444444' #declare default color
    Icon = IconManager()
    def SetTheme(self, theme):
        if theme == "Classic92": Theme.Classic92(self)
        elif theme == "AoHClassic": Theme.AoHClassic(self)

    def AoHClassic(self):
        Theme.IconColor = '#b17dff'
        themepath = os.path.join('cache', 'stylesheets', 'AoHClassic.css')
        print(themepath)
        file = QtCore.QFile(themepath)
        if file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            stream = QtCore.QTextStream(file)
            self.setStyleSheet(stream.readAll())
        
    def Classic92(self):
        Theme.IconColor = '#f2b036'
        themepath = os.path.join('cache', 'stylesheets', 'Classic92.css')
        print(themepath)
        file = QtCore.QFile(themepath)
        if file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            stream = QtCore.QTextStream(file)
            self.setStyleSheet(stream.readAll())
