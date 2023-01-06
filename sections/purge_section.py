from enum import Enum, auto

import tcod

from animation import Animation
from dialog import Dialog
from effects.horizontal_wipe_effect import HorizontalWipeDirection
from game_data.game_structure import chapters
from sections.section import Section
from sections.section_layouts import Rect, ImageRect, purge_section_info
from ui.purge_ui import PurgeUI
from typing import NamedTuple
from image import Image


class PurgeSectionStates(Enum):
    NONE = auto(),
    PENDING = auto(),
    INTRO = auto(),
    INSTRUCTION = auto(),
    

class PurgeSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "purge_section.xp", name) 
        self.ui = PurgeUI(self, self.tiles["graphic"])     
        self.seen_instructions = False

        # Pride Animations
        self.pride_dialog = Dialog(self, purge_section_info["pride_dialog_rect"], purge_section_info["text_color"], purge_section_info["dialog_fg"])
        frames = {"o":purge_section_info["pride_eyes_open"].image,"-":purge_section_info["pride_eyes_closed"].image}
        timeline = "oooooooooooooo-ooooooooo-oooooooo-ooooooooooooo-ooooooooooooooooo-o-oo"
        self.pride_eyes_animaton = Animation(self.engine, frames, timeline, 0.1)
        self.pride_eyes_animaton.start()
        
        frames = {"o":purge_section_info["pride_mouth_closed"].image,"-":purge_section_info["pride_mouth_open"].image}
        timeline = "o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-"
        self.pride_mouth_animaton = Animation(self.engine, frames, timeline, 0.1)

        # Member Animations
        self.member_dialog = Dialog(self, purge_section_info["member_dialog_rect"], purge_section_info["text_color"], purge_section_info["dialog_fg"])
        frames = {"o":"eo","-":"ec"}
        timeline = "oooooo-ooooooooooooooo-oo-oooooooooooooooo-ooooooooooooooooooo-ooooooo"
        self.member_eyes_animaton = Animation(self.engine, frames, timeline, 0.1)
        self.member_eyes_animaton.start()
        
        frames = {"o":"mo","-":"mc"}
        timeline = "o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-"
        self.member_mouth_animaton = Animation(self.engine, frames, timeline, 0.1)

        self.current_member = 1

    def update(self):
        super().update()
        self.time_into_state += self.engine.get_delta_time()

        if self.state == PurgeSectionStates.PENDING:
            if self.time_into_state >= purge_section_info["start_wait_time"]:
                self.change_state(PurgeSectionStates.INTRO)

        elif self.state == PurgeSectionStates.INTRO:
            self.update_dialog()
            if self.pride_dialog.is_finished() and not self.member_dialog.is_talking() and not self.member_dialog.is_finished():
                self.start_member_talking("Hello Thomas Pride, will you let me in?")

    def update_dialog(self):
        self.pride_dialog.update()
        if self.pride_dialog.is_finished():
            self.pride_mouth_animaton.stop()

        self.member_dialog.update()
        if self.member_dialog.is_finished():
            self.member_mouth_animaton.stop()

    def render(self, console):
        super().render(console)

        self.render_pride(console)
        self.render_pride_dialog(console)

        self.render_member(console)
        self.render_member_dialog(console)

        if self.state == PurgeSectionStates.INSTRUCTION:
            self.render_instructions(console)

        self.draw_button(console, purge_section_info["instructions_open_button"])
        self.draw_button(console, purge_section_info["pass_button"])
        self.draw_button(console, purge_section_info["bar_button"])
        self.draw_button(console, purge_section_info["roll_button"])
        self.render_ui(console)

    def render_pride_dialog(self, console):
        if self.should_render_pride_dialog():
            self.draw_image(console, purge_section_info["pride_speech_mark_image"].rect, purge_section_info["pride_speech_mark_image"].image)

            box_rect = purge_section_info["pride_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.pride_dialog.longest_line), max(4,self.pride_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, purge_section_info["dialog_decoration"],purge_section_info["dialog_margin"], purge_section_info["dialog_fg"],purge_section_info["dialog_bg"])

            self.pride_dialog.render(console)

    def render_pride(self, console):
        self.draw_image(console, purge_section_info["pride_character"].rect, purge_section_info["pride_character"].image)
        self.draw_image(console, purge_section_info["pride_eyes_open"].rect, self.pride_eyes_animaton.get_current_frame())
        if self.pride_dialog.is_talking():
            self.draw_image(console, purge_section_info["pride_mouth_open"].rect, self.pride_mouth_animaton.get_current_frame())
        else:
            self.draw_image(console, purge_section_info["pride_mouth_closed"].rect, purge_section_info["pride_mouth_closed"].image)

    def render_member_dialog(self, console):
        if self.should_render_member_dialog():
            self.draw_image(console, purge_section_info["member_speech_mark_image"].rect, purge_section_info["member_speech_mark_image"].image)

            box_rect = purge_section_info["member_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.member_dialog.longest_line), max(4,self.member_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, purge_section_info["dialog_decoration"],purge_section_info["dialog_margin"], purge_section_info["dialog_fg"],purge_section_info["dialog_bg"])

            self.member_dialog.render(console)

    def render_member(self, console):

        self.draw_image(console, purge_section_info["member_"+str(self.current_member)+"_character"].rect, purge_section_info["member_"+str(self.current_member)+"_character"].image)

        eyes_rect = purge_section_info["member_animation_rects"][self.member_eyes_animaton.get_current_frame()]
        eyes_image = purge_section_info["member_"+str(self.current_member)+"_frames"][self.member_eyes_animaton.get_current_frame()]
        self.draw_image(console, eyes_rect, eyes_image)
        
        if self.member_dialog.is_talking():
            mouth_rect = purge_section_info["member_animation_rects"]["mc"]
            mouth_image = purge_section_info["member_"+str(self.current_member)+"_frames"][self.member_mouth_animaton.get_current_frame()]
            self.draw_image(console, mouth_rect, mouth_image)
        else:
            mouth_rect = purge_section_info["member_animation_rects"][self.member_mouth_animaton.get_current_frame()]
            mouth_image = purge_section_info["member_"+str(self.current_member)+"_frames"]["mc"]
            self.draw_image(console, mouth_rect, mouth_image)

    def open(self):
        self.ui.setup_buttons()
        self.change_state(PurgeSectionStates.PENDING)        

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass

    def change_state(self, new_state):
        print("Changing to state:", new_state)
        self.state = new_state
        self.time_into_state = 0

        if new_state == PurgeSectionStates.INTRO:
            self.start_pride_talking("Hello, my name is Thomas Pride!")

        self.engine.set_full_screen_effect(self.engine.horizontal_wipe_effect, [HorizontalWipeDirection.RIGHT])
        self.engine.start_full_screen_effect()

    def open_instructions(self):
        self.pre_instructions_state = self.state
        self.seen_instructions = True
        self.change_state(PurgeSectionStates.INSTRUCTION)

    def close_instructions(self):
        self.change_state(self.pre_instructions_state)
        self.pre_instructions_state = None

    def render_instructions(self, console):
        self.draw_image(console, purge_section_info["instructions_image"].rect, purge_section_info["instructions_image"].image)
        self.draw_button(console, purge_section_info["instructions_close_button"])

    def should_render_pride_dialog(self):
        return self.pride_dialog.is_talking() or self.pride_dialog.is_finished()

    def start_pride_talking(self, text):
        self.pride_dialog.start_talking(text)
        self.pride_mouth_animaton.start()

    def should_render_member_dialog(self):
        return self.member_dialog.is_talking() or self.member_dialog.is_finished()

    def start_member_talking(self, text):
        self.member_dialog.start_talking(text)
        self.member_mouth_animaton.start()
