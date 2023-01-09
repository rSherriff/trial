from enum import Enum, auto
from typing import NamedTuple

import tcod

from animation import Animation
from dialog import Dialog
from effects.horizontal_move_effect import (HorizontalMoveDirection,
                                            HorizontalMoveEffect)
from game_data.game_structure import chapters
from image import Image
from sections.section import Section
from sections.section_layouts import ImageRect, Rect, purge_section_info
from ui.purge_ui import PurgeUI


class PurgeSectionStates(Enum):
    NONE = auto(),
    PENDING = auto(),
    INTRO = auto(),
    INSTRUCTION = auto(),
    GAME_SETUP = auto(),
    GAME = auto(),
    GAME_TRANSITION = auto(),
    

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

        # Effects
        self.member_move_effect = HorizontalMoveEffect(self.engine, 0,0,0,0)

        self.current_member = 0

    def update(self):
        super().update()
        self.time_into_state += self.engine.get_delta_time()

        if self.state == PurgeSectionStates.PENDING:
            if self.time_into_state >= purge_section_info["start_wait_time"]:
                self.change_state(PurgeSectionStates.INTRO)

        elif self.state == PurgeSectionStates.INTRO:
            self.change_state(PurgeSectionStates.GAME_SETUP)

        elif self.state == PurgeSectionStates.GAME_SETUP:
            if not self.member_move_effect.in_effect: 
                self.change_state(PurgeSectionStates.GAME)

        elif self.state == PurgeSectionStates.GAME:
            self.update_dialog()

        elif self.state == PurgeSectionStates.GAME_TRANSITION:
            if not self.member_move_effect.in_effect: 
                self.change_state(PurgeSectionStates.GAME_SETUP)

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

        self.render_effects(console)

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
        if self.should_render_pride():
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
        if self.should_render_member():
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

    def render_effects(self,console):
        if self.member_move_effect.in_effect:
            self.member_move_effect.render(console)

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
        if key == tcod.event.K_q:
            self.change_state(PurgeSectionStates.GAME_TRANSITION)

    def change_state(self, new_state):
        print("Changing to state:", new_state)
        self.state = new_state
        self.time_into_state = 0

        if new_state == PurgeSectionStates.INTRO:
            pass
        elif new_state == PurgeSectionStates.GAME_SETUP:
            self.pick_member()

            member_rect = purge_section_info["member_"+str(self.current_member)+"_character"].rect
            member_image = purge_section_info["member_"+str(self.current_member)+"_character"].image

            eyes_rect = purge_section_info["member_animation_rects"][self.member_eyes_animaton.get_current_frame()]
            eyes_image = purge_section_info["member_"+str(self.current_member)+"_frames"]["eo"]

            mouth_rect = purge_section_info["member_animation_rects"][self.member_mouth_animaton.get_current_frame()]
            mouth_image = purge_section_info["member_"+str(self.current_member)+"_frames"]["mc"]

            self.member_move_effect = HorizontalMoveEffect(self.engine, member_rect.x,member_rect.y,member_rect.width,member_rect.height)

            temp_console = tcod.Console(width=self.member_move_effect.width, height=self.member_move_effect.height, order="F")
            temp_console.tiles_rgb[0: member_rect.width,0:  member_rect.height] = member_image.tiles[0: member_rect.width, 0: member_rect.height]["graphic"]
            temp_console.tiles_rgb[4: 4+eyes_rect.width,3:  3+eyes_rect.height] = eyes_image.tiles[0: eyes_rect.width, 0: eyes_rect.height]["graphic"]
            temp_console.tiles_rgb[5: 5+mouth_rect.width,6:  6+mouth_rect.height] = mouth_image.tiles[0: mouth_rect.width, 0: mouth_rect.height]["graphic"]

            self.member_move_effect.set_tiles(temp_console.tiles)
            self.member_move_effect.start([HorizontalMoveDirection.IN_LEFT])

        elif new_state == PurgeSectionStates.GAME:
            self.start_member_talking("Hello, I've just arrived!")

        elif new_state == PurgeSectionStates.GAME_TRANSITION:
            self.member_dialog.reset_talking()
            self.pride_dialog.reset_talking()

            member_rect = purge_section_info["member_"+str(self.current_member)+"_character"].rect
            member_image = purge_section_info["member_"+str(self.current_member)+"_character"].image

            eyes_rect = purge_section_info["member_animation_rects"][self.member_eyes_animaton.get_current_frame()]
            eyes_image = purge_section_info["member_"+str(self.current_member)+"_frames"]["eo"]

            mouth_rect = purge_section_info["member_animation_rects"][self.member_mouth_animaton.get_current_frame()]
            mouth_image = purge_section_info["member_"+str(self.current_member)+"_frames"]["mc"]

            self.member_move_effect = HorizontalMoveEffect(self.engine, member_rect.x,member_rect.y,member_rect.width,member_rect.height)

            temp_console = tcod.Console(width=self.member_move_effect.width, height=self.member_move_effect.height, order="F")
            temp_console.tiles_rgb[0: member_rect.width,0:  member_rect.height] = member_image.tiles[0: member_rect.width, 0: member_rect.height]["graphic"]
            temp_console.tiles_rgb[4: 4+eyes_rect.width,3:  3+eyes_rect.height] = eyes_image.tiles[0: eyes_rect.width, 0: eyes_rect.height]["graphic"]
            temp_console.tiles_rgb[5: 5+mouth_rect.width,6:  6+mouth_rect.height] = mouth_image.tiles[0: mouth_rect.width, 0: mouth_rect.height]["graphic"]
            self.member_move_effect.set_tiles(temp_console.tiles)
            self.member_move_effect.start([HorizontalMoveDirection.OUT_LEFT])

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

    def should_render_pride(self):
        return self.state == PurgeSectionStates.GAME_SETUP or self.state == PurgeSectionStates.GAME or self.state == PurgeSectionStates.GAME_TRANSITION

    def should_render_pride_dialog(self):
        return self.pride_dialog.is_talking() or self.pride_dialog.is_finished()

    def start_pride_talking(self, text):
        self.pride_dialog.start_talking(text)
        self.pride_mouth_animaton.start()

    def should_render_member(self):
        return self.state == self.state == PurgeSectionStates.GAME

    def should_render_member_dialog(self):
        return self.member_dialog.is_talking() or self.member_dialog.is_finished()

    def start_member_talking(self, text):
        self.member_dialog.start_talking(text)
        self.member_mouth_animaton.start()

    def pick_member(self):
        self.current_member = 1
