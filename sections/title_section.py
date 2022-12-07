from sections.section import Section
from dialog import Dialog
from sections.section_layouts import title_section_info

class TitleSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        super().__init__(engine, x, y, width, height, "title_section.xp")      
        self.dialog = Dialog(self, title_section_info["main_text"])

    def update(self):
        super().update()
        self.dialog.update()
    
    def render(self, console):
        super().render(console)
        self.dialog.render(console)

    def open(self, title, text):
        self.title = title
        self.text = text
        self.dialog.start_character_talking(self.text)

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass