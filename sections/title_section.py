from enum import Enum, auto

import tcod

from actions.game_actions import JumpToStageAction
from dialog import Dialog
from effects.horizontal_wipe_effect import HorizontalWipeDirection
from sections.section import Section
from sections.section_layouts import title_section_info
from ui.title_ui import TitleUI
from utils.color import blend_colour
from utils.utils import lerp


class TitleSectionState(Enum):
    START_WAIT = auto()
    TITLE = auto(),
    TEXT = auto(),
    PAUSE = auto(),
    BUTTON = auto(),

class TitleSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "title_section.xp", name)      
        self.dialog = Dialog(self, title_section_info["main_text"])
        self.ui = None
        self.change_state(TitleSectionState.START_WAIT)

    def update(self):
        super().update()
        self.dialog.update()
        self.time_into_section += self.engine.get_delta_time()

        if self.state == TitleSectionState.TITLE:
            if self.time_into_section > title_section_info["title_time"]:
                self.change_state(TitleSectionState.TEXT)

        elif self.state == TitleSectionState.TEXT:
            if self.dialog.is_finished():
                self.change_state(TitleSectionState.PAUSE)

        elif self.state == TitleSectionState.PAUSE:
            if self.time_into_section > title_section_info["text_pause_time"]:
                self.change_state(TitleSectionState.BUTTON)

        elif self.state == TitleSectionState.BUTTON:
            pass
    
    def render(self, console):
        super().render(console)

        title_rect = title_section_info["title"]
        if self.state == TitleSectionState.START_WAIT:
            if self.time_into_section >= title_section_info["start_wait_time"]:
                self.change_state(TitleSectionState.TITLE)
        elif self.state == TitleSectionState.TITLE:
            if self.time_into_section <= title_section_info["title_fade_time"]:
                t = self.time_into_section / title_section_info["title_fade_time"]
                title_color = blend_colour(title_section_info["text_color"], (0,0,0), t)
            else:
                title_color = title_section_info["text_color"]
            console.print_box(title_rect.x, title_rect.y, title_rect.width, title_rect.height, self.title, alignment=tcod.CENTER, fg=title_color)

        elif self.state == TitleSectionState.TEXT or self.state == TitleSectionState.PAUSE:
            console.print_box(title_rect.x, title_rect.y, title_rect.width, title_rect.height, self.title, alignment=tcod.CENTER, fg=title_section_info["text_color"])
            self.dialog.render(console)

        elif self.state == TitleSectionState.BUTTON:
            console.print_box(title_rect.x, title_rect.y, title_rect.width, title_rect.height, self.title, alignment=tcod.CENTER, fg=title_section_info["text_color"])
            self.dialog.render(console)
            self.draw_button(console, title_section_info["start_button"])
            self.render_ui(console)
        
    
    def open(self, chapter):
        self.change_state(TitleSectionState.START_WAIT)
        self.title = chapter["title"]
        self.text = chapter["text"]
        self.stage = chapter["stage"]
        self.ui = None
        
        
    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        if key == tcod.event.K_ESCAPE or key == tcod.event.K_SPACE:
            self.skip_to_end()
        elif key == tcod.event.K_RETURN:
            if self.state != TitleSectionState.BUTTON:
                self.skip_to_end()
            else:
                JumpToStageAction(self.engine, self.stage).perform()
        
    def change_state(self, new_state):
        self.time_into_section = 0
        self.state = new_state

        if new_state == TitleSectionState.TEXT:
            self.dialog.start_talking(self.text)
        elif new_state == TitleSectionState.BUTTON:
            self.ui = TitleUI(self, self.tiles["graphic"])
            self.ui.setup_buttons(self.stage)
            self.engine.set_full_screen_effect(self.engine.horizontal_wipe_effect, [HorizontalWipeDirection.RIGHT])
            self.engine.start_full_screen_effect()


    def skip_to_end(self):
        self.change_state(TitleSectionState.BUTTON)
        if self.dialog.is_pending():
            self.dialog.start_talking(self.text)
        self.dialog.end_talking()
