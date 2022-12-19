from enum import Enum, auto

import tcod

from animation import Animation
from dialog import Dialog
from game_data.game_structure import chapters
from sections.section import Section
from sections.section_layouts import Rect, hunt_section_info
from ui.hunt_ui import HuntUI


class HuntSectionStates(Enum):
    NONE = auto(),
    PENDING = auto(),
    INTRO = auto(),
    INSTRUCTION = auto(),
    PLAYING = auto(),

class HuntSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "hunt_section.xp", name) 
        self.ui = HuntUI(self, self.tiles["graphic"])     

        self.advisor_dialog = Dialog(self, hunt_section_info["advisor_dialog_rect"], hunt_section_info["advisor_dialog_text_color"], hunt_section_info["advisor_dialog_fg"])
        self.state = HuntSectionStates.NONE
        self.time_into_state = 0

        frames = {"o":hunt_section_info["advisor_top_eyes_open"].image,"-":hunt_section_info["advisor_top_eyes_closed"].image}
        timeline = "oooooooooooooo-ooooooooo-oooooooo-ooooooooooooo-ooooooooooooooooo-o-oo"
        self.advisor_top_animaton = Animation(self.engine, frames, timeline, 0.1)
        self.advisor_top_animaton.start()

        frames = {"o":hunt_section_info["advisor_btm_mouth_closed"].image,"-":hunt_section_info["advisor_btm_mouth_open"].image}
        timeline = "o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-"
        self.advisor_btm_animaton = Animation(self.engine, frames, timeline, 0.1)

    def update(self):
        super().update()

        self.time_into_state += self.engine.get_delta_time()

        if self.state == HuntSectionStates.PENDING:
            if self.time_into_state >= hunt_section_info["start_wait_time"]:
                self.change_state(HuntSectionStates.INTRO)

        elif self.state == HuntSectionStates.INTRO:
            self.advisor_dialog.update()
            if self.advisor_dialog.is_finished():
                self.advisor_btm_animaton.stop()

    
    def render(self, console):
        super().render(console)

        if self.state == HuntSectionStates.PENDING:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)

        elif self.state == HuntSectionStates.INTRO:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())

            if self.advisor_dialog.is_talking():
                self.draw_image(console, hunt_section_info["advisor_btm_mouth_open"].rect, self.advisor_btm_animaton.get_current_frame())
            else:
                self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)
            
            self.draw_image(console, hunt_section_info["speech_mark_image"].rect, hunt_section_info["speech_mark_image"].image)

            box_rect = hunt_section_info["advisor_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.advisor_dialog.longest_line), max(4,self.advisor_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, hunt_section_info["advisor_dialog_decoration"],hunt_section_info["advisor_dialog_margin"], hunt_section_info["advisor_dialog_fg"],hunt_section_info["advisor_dialog_bg"])

            self.advisor_dialog.render(console)

        elif self.state == HuntSectionStates.INSTRUCTION:
            self.draw_image(console, hunt_section_info["instructions_image"].rect, hunt_section_info["instructions_image"].image)
            self.draw_button(console, hunt_section_info["instructions_close_button"])

        elif self.state == HuntSectionStates.PLAYING:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)
            self.draw_button(console, hunt_section_info["instructions_open_button"])

        self.draw_button(console, hunt_section_info["quit_button"])
        self.render_ui(console)

    def open(self):
        self.ui.setup_buttons()
        self.change_state(HuntSectionStates.PENDING)        

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        if self.state == HuntSectionStates.INTRO:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            else:
                self.change_state(HuntSectionStates.PLAYING)

    def keydown(self, key):
        if key == tcod.event.K_ESCAPE or key == tcod.event.K_SPACE or key == tcod.event.K_RETURN:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            if self.state == HuntSectionStates.INSTRUCTION:
                self.change_state(HuntSectionStates.PLAYING)

    def change_state(self, new_state):
        self.state = new_state
        self.time_into_state = 0

        if new_state == HuntSectionStates.PENDING:
            self.ui.instructions_open_button.disable()
            self.ui.instructions_close_button.disable()
        elif new_state == HuntSectionStates.INTRO:
            self.advisor_dialog.start_talking(chapters["hunt"]["intro"])
            self.ui.instructions_open_button.disable()
            self.advisor_btm_animaton.start()
        elif new_state == HuntSectionStates.INSTRUCTION:
            self.ui.instructions_open_button.disable()
            self.ui.instructions_close_button.enable()
            self.ui.quit_button.disable()
        else:
            self.advisor_dialog.reset_talking()
            self.ui.instructions_open_button.enable()
            self.ui.instructions_close_button.disable()
            self.ui.quit_button.enable()

    def open_instructions(self):
        self.change_state(HuntSectionStates.INSTRUCTION)

    def close_instructions(self):
        self.change_state(HuntSectionStates.PLAYING)