from sections.section import Section

class HuntSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        super().__init__(engine, x, y, width, height, "england.xp")      

    def update(self):
        super().update()
    
    def render(self, console):
        super().render(console)

    def open(self):
        pass

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass