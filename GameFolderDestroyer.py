import os
import shutil
from PyQt5.QtCore import QObject, pyqtSignal

# Найти способ удалять все из папки, кроме config. Илиже найти способ как-то сохронять config. 
# Мой варинт решения. Сделать конфиг вынесенным в отдельную папку в папке .AoH Luncher и проверять наличие майнрафта не по папке .AoHLauncher, а по внутренней папки.
# По типу как мы это делали с folder_version

class ConsoleMessageClass(QObject):
    message_signal = pyqtSignal(str)
    
    def Send (self, message):
        self.message_signal.emit(message)
        
ConsoleMessage = ConsoleMessageClass() # создаю экземпляр чтобы можно было потом выгрузить его в Main
def GetConsoleMessage():
    return ConsoleMessage

class MinecraftDestroyer:
    @staticmethod
    def DestroyIt():
        ConsoleMessage.Send("Start the process of deleting minecraft...")
        # Указываем кодировку utf-8 для работы с файловой системой
        os.chdir(os.path.join(os.getenv('APPDATA')))  
        minecraft_path = '.AoHLauncher'
        # print(os.path.isdir(minecraft_path))
        
        if os.path.exists(minecraft_path):
            shutil.rmtree(minecraft_path)  # Используем shutil.rmtree для удаления папки рекурсивно
            ConsoleMessage.Send(f"Folder {minecraft_path} has been sucess deleted.")
        else:
            ConsoleMessage.Send(f"Folder {minecraft_path} isn't exists.")
            # ConsoleMessage.Send("Or launcher can't find it!")