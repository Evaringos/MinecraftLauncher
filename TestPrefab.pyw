import minecraft_launcher_lib
import subprocess

version = input("Enter minecraft version: ")
username = input("Enter Username: ")

minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=".AoHLauncher")

options = {
    "username": username,
    "uuid": "",
    "token": ""
}

subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=version, minecraft_directory=".AoHLauncher", options=options))