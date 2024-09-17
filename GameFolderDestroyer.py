import os
import shutil

minecraft_path = os.path.join(os.getenv('APPDATA'), '.AoHLauncher')
print(os.path.isdir(minecraft_path))

if os.path.exists(minecraft_path):
    shutil.rmtree(minecraft_path)
    print(f"Папка {minecraft_path} удалена.")
else:
    print(f"Папка {minecraft_path} не существует.")