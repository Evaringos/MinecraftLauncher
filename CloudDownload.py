import os
import wget
import zipfile

class CloudDownload():
    def __init__(self, zipname:str, downpath:str, extractpath:str):
        zippath = os.path.join(downpath, zipname)
        download = 'https://drive.usercontent.google.com/download?id=1tivakclkSn_z85SoywIw87www5X35Y8S&export=download&authuser=0&confirm=t'
        wget.download(url=download, out=downpath)
        with zipfile.ZipFile(zippath, 'r') as zip_file:
            zip_file.extractall(extractpath)
        os.remove(zippath)
