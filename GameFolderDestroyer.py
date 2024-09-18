import os
import shutil

class MinecraftDestroyer:
    @staticmethod
    def DestroyIt():
        # Указываем кодировку utf-8 для работы с файловой системой
        os.chdir(os.path.join(os.getenv('APPDATA')))  
        minecraft_path = '.AoHLauncher'
        # print(os.path.isdir(minecraft_path))
        
        if os.path.exists(minecraft_path):
            shutil.rmtree(minecraft_path)  # Используем shutil.rmtree для удаления папки рекурсивно
            print(f"Папка {minecraft_path} удалена.")
        else:
            print(f"Папка {minecraft_path} не существует.")