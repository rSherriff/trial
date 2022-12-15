from enum import Enum, auto

from animation import Animation
from dialog import Dialog
from game_data.game_structure import chapters
from sections.section import Section
from sections.section_layouts import Rect, hunt_section_info
from ui.hunt_ui import HuntUI


class HuntSectionStates(Enum):
    NONE = auto(),
    PENDING = auto(),
    INSTRUCTION = auto(),
    PLAYING = auto(),

class HuntSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "hunt_section.xp", name) 
        self.ui = HuntUI(self, self.tiles["graphic"])     

        self.instruction_dialog = Dialog(self, hunt_section_info["instruction_dialog_rect"], hunt_section_info["instruction_dialog_text_color"], hunt_section_info["instruction_dialog_fg"])
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
                self.change_state(HuntSectionStates.INSTRUCTION)

        elif self.state == HuntSectionStates.INSTRUCTION:
            self.instruction_dialog.update()
            if self.instruction_dialog.is_finished():
                self.advisor_btm_animaton.stop()

    
    def render(self, console):
        super().render(console)

        if self.state == HuntSectionStates.PENDING:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)

        elif self.state == HuntSectionStates.INSTRUCTION:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())

            if self.instruction_dialog.is_talking():
                self.draw_image(console, hunt_section_info["advisor_btm_mouth_open"].rect, self.advisor_btm_animaton.get_current_frame())
            else:
                self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)
            
            self.draw_image(console, hunt_section_info["speech_mark_image"].rect, hunt_section_info["speech_mark_image"].image)

            box_rect = hunt_section_info["instruction_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.instruction_dialog.longest_line), max(4,self.instruction_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, hunt_section_info["instruction_dialog_decoration"],hunt_section_info["instruction_dialog_margin"], hunt_section_info["instruction_dialog_fg"],hunt_section_info["instruction_dialog_bg"])

            self.instruction_dialog.render(console)

        elif self.state == HuntSectionStates.PLAYING:
            self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)
            self.draw_button(console, hunt_section_info["instructions_button"])

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
        if self.state == HuntSectionStates.INSTRUCTION:
            self.change_state(HuntSectionStates.PLAYING)

    def keydown(self, key):
        pass

    def change_state(self, new_state):
        self.state = new_state
        self.time_into_state = 0

        if new_state == HuntSectionStates.INSTRUCTION:
            self.instruction_dialog.start_talking(chapters["hunt"]["instruction"])
            self.ui.instructions_button.disable()
            self.advisor_btm_animaton.start()
        else:
            self.instruction_dialog.reset_talking()
            self.ui.instructions_button.enable()

    def open_instructions(self):
        self.change_state(HuntSectionStates.INSTRUCTION)