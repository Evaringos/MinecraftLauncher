class Theme:
    DEFAULT_THEME="AoHClassic"
    
    def __init__(self, theme=None):
        self.SetTheme(theme or self.DEFAULT_THEME)

    def SetTheme(self, theme):
        if theme == "AoHClassic":
            self.AoHClassic()
        elif theme == "Classic92":
            self.Classic92()
        else:
            raise ValueError(f"Unknown theme: {theme}")

    def AoHClassic(self):
        self.ColAccent = "#f2b036"
        self.ColBg = "#191919"
    
    def Classic92(self):
        self.ColAccent = "#f2b036"
        self.ColBg = "#eaeaea"
