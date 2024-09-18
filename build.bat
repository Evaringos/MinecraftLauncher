del AoHLauncher.exe
pyinstaller --noconfirm --noconsole --onefile ^
	--name=AoHLauncher ^
	--distpath=. ^
	--icon=cache/aoh_icon.ico ^
	--add-data="cache/aoh_icon.ico;cache" ^
	--add-data="cache/Launcher_logo.png;cache" ^
	MainLauncher.py