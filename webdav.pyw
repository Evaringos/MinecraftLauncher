from webdav3.client import Client
options = {
    'webdav_hostname' : "https://webdav.yandex.ru/minecraft",
    'webdav_login' : "Stradlater.25",
    'webdav_password' : "rdkrswobzpiqfbht"
}
client = Client(options)

files = client.list("mods/")

print (files)

print("Downloading mods...\n")
client.download_sync(remote_path="mods/*", local_path="./")
print("Completed")

    





    

    






