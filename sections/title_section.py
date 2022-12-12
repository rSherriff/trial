import tcod
from sections.section import Section
from dialog import Dialog
from sections.section_layouts import title_section_info
from ui.title_ui import TitleUI

class TitleSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        super().__init__(engine, x, y, width, height, "title_section.xp")      
        self.dialog = Dialog(self, title_section_info["main_text"])
        self.ui = TitleUI(self, self.tiles["graphic"])

    def update(self):
        super().update()
        self.dialog.update()
    
    def render(self, console):
        super().render(console)
        title_rect = title_section_info["title"]
        console.print_box(title_rect.x, title_rect.y, title_rect.width, title_rect.height, self.title, alignment=tcod.CENTER)
        self.dialog.render(console)
        self.draw_button(console, title_section_info["start_button"])
        self.render_ui(console)

    def open(self, chapter):
        self.title = chapter["title"]
        self.text = chapter["text"]
        self.ui.setup_buttons(chapter["stage"])
        self.dialog.start_character_talking(self.text)

    def draw_button(self, console, bs):
        console.draw_frame(bs.x,bs.y,bs.width,bs.height, decoration=bs.decoration, bg=bs.bg, fg=bs.fg)
        console.print_box(bs.x+1,bs.y+1,bs.width-2,bs.height-2,string=bs.text,alignment=tcod.CENTER, bg=bs.font_bg, fg=bs.font_fg)

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass