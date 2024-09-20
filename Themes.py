from PyQt5 import QtWidgets, QtCore

class ThemeNew(QtWidgets.QMainWindow):
    def __init__(self):
        super(ThemeNew,self).self.__init__()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)  # Set the timer to fire every 50ms
        
        
    def SetTheme(self, theme):
        if theme == "Classic92": ThemeNew.Classic92(self)
        elif theme == "AoHClassic": ThemeNew.AoHClassic(self)

    def AoHClassic(self):
        file = QtCore.QFile("cache/stylesheets/AoHClassic.css")
        if file.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            stream = QtCore.QTextStream(file)
            self.setStyleSheet(stream.readAll())
        
    def Classic92(self):
        file = QtCore.QFile("cache/stylesheets/Classic92.css")
        if file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            stream = QtCore.QTextStream(file)
            self.setStyleSheet(stream.readAll())

