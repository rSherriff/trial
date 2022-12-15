from sections.section import Section
from ui.hunt_ui import HuntUI
from sections.section_layouts import hunt_section_info

class HuntSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "hunt_section.xp", name) 
        self.ui = HuntUI(self, self.tiles["graphic"])     

    def update(self):
        super().update()
    
    def render(self, console):
        super().render(console)
        self.draw_button(console, hunt_section_info["quit_button"])
        self.render_ui(console)

    def open(self):
        self.ui.setup_buttons()

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass