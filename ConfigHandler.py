import os
import configparser

minecraft_path = os.path.expanduser('~\\AppData\\Roaming\\.AoHLauncher')
aoh_config_file = os.path.join(minecraft_path, "AoHConfig.ini")

def create_default_config():
    config = configparser.ConfigParser()
    config['Launcher'] = {
        'username': '',
        'theme': 'Classic92'
    }
    with open(aoh_config_file, 'w') as configfile:
        config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    config.read(aoh_config_file)
    return config

def update_config(section, key, new_value):
    config = read_config()

    # Проверяем, существует ли секция
    if section not in config:
        raise ValueError(f"Секция '{section}' не найдена в конфигурационном файле")

    # Проверяем, существует ли ключ в секции
    if key not in config[section]:
        raise ValueError(f"Ключ '{key}' не найден в секции '{section}'")
    
    config[section][key] = new_value
        
    with open(aoh_config_file, 'w') as configfile:
        config.write(configfile)

'''
Примеры (можно одиночные кавычки)
Ввод в конфиг:
update_config("Launcher", "Username", "Steve")

Получится следующее:
---
[Launcher]
Username = steve
--

Чтение из конфига:
config["Launcher"]["Username"]
'''
