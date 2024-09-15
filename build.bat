del AoHLauncher.exe
pyinstaller --noconfirm --noconsole --onefile ^
	--name=AoHLauncher ^
	--distpath=. ^
	--icon=cache/aoh_icon.ico ^
	--add-data="cache/aoh_icon.ico;cache" ^
	--add-data="cache/close.png;cache" ^
	--add-data="cache/folder.png;cache" ^
	--add-data="cache/hide.png;cache" ^
	--add-data="cache/Launcher_logo.png;cache" ^
	--add-data="cache/settings.png;cache" ^
	TestLauncherDesign.py