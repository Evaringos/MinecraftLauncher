import GameLauncher
import configparser

def create_default_config():
    config = configparser.ConfigParser()
    config['Launcher'] = {
        'username': '',
        'theme': 'AoHClassic',
        'ram': '4'
    }
    with open(GameLauncher.aoh_config_file, 'w') as configfile:
        config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    config.read(GameLauncher.aoh_config_file)
    return config

def update_config(section, key, new_value):
    config = read_config()
    if section not in config:
        raise ValueError(f"Секция '{section}' не найдена в конфигурационном файле")
    if key not in config[section]:
        raise ValueError(f"Ключ '{key}' не найден в секции '{section}'")
    
    config[section][key] = new_value
    with open(GameLauncher.aoh_config_file, 'w') as configfile:
        config.write(configfile)

''' Примеры
Ввод в конфиг:  update_config("Launcher", "username", "Steve")

Получится следующее:
+----------------+
|[Launcher]      |
|username = Steve|
+----------------+

Чтение из конфига:  config["Launcher"]["Username"]'''



