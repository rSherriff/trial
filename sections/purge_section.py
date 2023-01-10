from enum import Enum, auto
from threading import Timer
from typing import NamedTuple

import tcod

from animation import Animation
from dialog import Dialog
from effects.horizontal_move_effect import (HorizontalMoveDirection,
                                            HorizontalMoveEffect)
from effects.horizontal_wipe_effect import HorizontalWipeDirection
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
    GAME_MEMBER_DIALOG = auto(),
    GAME = auto(),
    GAME_PRIDE_DIALOG = auto(),
    GAME_TRANSITION = auto(),

class PurgeSectionPerson(Enum):
    MEMBER = auto()
    PRIDE = auto()

class Member(NamedTuple):
    id: InterruptedError
    name: str
    dialog: str
    should_be_barred: bool

test_member = Member(1, "Richard Sherriff", "Hello, can you let me in please?", True)

members = [
    test_member
]
    

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
        self.pride_move_effect = HorizontalMoveEffect(self.engine, 0,0,0,0)
        self.member_move_effect = HorizontalMoveEffect(self.engine, 0,0,0,0)

        self.current_member = 0
        self.barred_members = 0
        self.passed_members = 0

        self.state_end_timer = None

        self.state = PurgeSectionStates.PENDING

    def update(self):
        super().update()
        self.time_into_state += self.engine.get_delta_time()

        if self.state == PurgeSectionStates.PENDING:
            if self.time_into_state >= purge_section_info["start_wait_time"]:
                self.change_state(PurgeSectionStates.INTRO)

        elif self.state == PurgeSectionStates.INTRO:
            if not self.pride_move_effect.in_effect: 
                self.change_state(PurgeSectionStates.GAME_SETUP)

        elif self.state == PurgeSectionStates.GAME_SETUP:
            if not self.member_move_effect.in_effect: 
                self.change_state(PurgeSectionStates.GAME_MEMBER_DIALOG)

        elif self.state == PurgeSectionStates.GAME_MEMBER_DIALOG:
            self.update_dialog()
            if self.member_dialog.is_finished() and self.state_end_timer == None: 
                self.state_end_timer = Timer(purge_section_info["member_dialog_wait_time"], self.change_state, [PurgeSectionStates.GAME])
                self.state_end_timer.start()

        elif self.state == PurgeSectionStates.GAME:
            pass

        elif self.state == PurgeSectionStates.GAME_PRIDE_DIALOG:
            self.update_dialog()
            if self.pride_dialog.is_finished() and self.state_end_timer == None: 
                self.state_end_timer = Timer(purge_section_info["pride_dialog_wait_time"], self.change_state, [PurgeSectionStates.GAME_TRANSITION])
                self.state_end_timer.start()

        elif self.state == PurgeSectionStates.GAME_TRANSITION:
            if not self.member_move_effect.in_effect and self.state_end_timer == None: 
                self.state_end_timer = Timer(purge_section_info["transition_wait_time"], self.change_state, [PurgeSectionStates.GAME_SETUP])
                self.state_end_timer.start()

    def update_dialog(self):
        self.pride_dialog.update()
        if self.pride_dialog.is_finished():
            self.pride_mouth_animaton.stop()

        self.member_dialog.update()
        if self.member_dialog.is_finished():
            self.member_mouth_animaton.stop()

    def render(self, console):
        super().render(console)

        # Render Pride
        self.render_character(console, PurgeSectionPerson.PRIDE)
        self.render_dialog(console, PurgeSectionPerson.PRIDE)

        # Render Member
        self.render_character(console, PurgeSectionPerson.MEMBER)
        self.render_dialog(console, PurgeSectionPerson.MEMBER)

        self.render_effects(console)

        if self.state == PurgeSectionStates.INSTRUCTION:
            self.render_instructions(console)

        self.render_ui(console)

    def render_dialog(self, console, person_type: PurgeSectionPerson):
        if (person_type == PurgeSectionPerson.PRIDE and self.should_render_pride_dialog()) or (person_type == PurgeSectionPerson.MEMBER and self.should_render_member_dialog()):
            speech_mark_key = "pride_speech_mark_image" if person_type == PurgeSectionPerson.PRIDE else "member_speech_mark_image"
            self.draw_image(console, purge_section_info[speech_mark_key].rect, purge_section_info[speech_mark_key].image)

            box_rect = purge_section_info["pride_dialog_rect" if person_type == PurgeSectionPerson.PRIDE else "member_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.pride_dialog.longest_line), max(4,self.pride_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, purge_section_info["dialog_decoration"],purge_section_info["dialog_margin"], purge_section_info["dialog_fg"],purge_section_info["dialog_bg"])

            if person_type == PurgeSectionPerson.PRIDE:
                self.pride_dialog.render(console)  
            else:
                self.member_dialog.render(console)

    def render_character(self, console, person_type: PurgeSectionPerson):
        if (person_type == PurgeSectionPerson.PRIDE and self.should_render_pride()) or (person_type == PurgeSectionPerson.MEMBER and self.should_render_member()):
            member = members[self.current_member]

            character_key = "pride_character" if person_type == PurgeSectionPerson.PRIDE else "member_"+str(member.id)+"_character"
            self.draw_image(console, purge_section_info[character_key].rect, purge_section_info[character_key].image)

            if person_type == PurgeSectionPerson.PRIDE:
                self.draw_image(console, purge_section_info["pride_eyes_open"].rect, self.pride_eyes_animaton.get_current_frame())

                if self.pride_dialog.is_talking():
                    self.draw_image(console, purge_section_info["pride_mouth_open"].rect, self.pride_mouth_animaton.get_current_frame())
                else:
                    self.draw_image(console, purge_section_info["pride_mouth_closed"].rect, purge_section_info["pride_mouth_closed"].image)
            else:
                eyes_rect = purge_section_info["member_animation_rects"][self.member_eyes_animaton.get_current_frame()]
                eyes_image = purge_section_info["member_"+str(member.id)+"_frames"][self.member_eyes_animaton.get_current_frame()]
                self.draw_image(console, eyes_rect, eyes_image)

                if self.member_dialog.is_talking():
                    mouth_rect = purge_section_info["member_animation_rects"]["mc"]
                    mouth_image = purge_section_info["member_"+str(member.id)+"_frames"][self.member_mouth_animaton.get_current_frame()]
                    self.draw_image(console, mouth_rect, mouth_image)
                else:
                    mouth_rect = purge_section_info["member_animation_rects"][self.member_mouth_animaton.get_current_frame()]
                    mouth_image = purge_section_info["member_"+str(member.id)+"_frames"]["mc"]
                    self.draw_image(console, mouth_rect, mouth_image)

    def render_effects(self,console):
        if self.member_move_effect.in_effect:
            self.member_move_effect.render(console)
        if self.pride_move_effect.in_effect:
            self.pride_move_effect.render(console)

    def render_ui(self, console):
        self.draw_button(console, purge_section_info["instructions_open_button"])
        self.draw_button(console, purge_section_info["roll_button"])

        if self.state == PurgeSectionStates.GAME and self.member_dialog.is_finished():
            self.draw_button(console, purge_section_info["pass_button"])
            self.draw_button(console, purge_section_info["bar_button"])

        if not self.ui is None:
            self.ui.render(console)

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

        self.state_end_timer = None

        # Exit State
        old_state = self.state
        if old_state == PurgeSectionStates.GAME:
            self.ui.pass_button.disable()
            self.ui.bar_button.disable()

        self.state = new_state
        self.time_into_state = 0

        # Enter State
        if new_state == PurgeSectionStates.PENDING:
            self.ui.pass_button.disable()
            self.ui.bar_button.disable()
            self.ui.instructions_close_button.disable()

        elif new_state == PurgeSectionStates.INTRO:
            effect_image = self.prepare_pride_effect()
            self.pride_move_effect.set_tiles(effect_image.tiles)
            self.pride_move_effect.start([HorizontalMoveDirection.IN_RIGHT])

        elif new_state == PurgeSectionStates.GAME_SETUP:
            self.pick_member()

            effect_image = self.prepare_member_effect()
            self.member_move_effect.set_tiles(effect_image.tiles)
            self.member_move_effect.start([HorizontalMoveDirection.IN_LEFT])

        elif new_state == PurgeSectionStates.GAME_MEMBER_DIALOG:
            member = members[self.current_member]
            self.start_member_talking(member.dialog)

        elif new_state == PurgeSectionStates.GAME:

            if not self.seen_instructions:
                self.open_instructions()
                return

            self.ui.pass_button.enable()
            self.ui.bar_button.enable()
            self.engine.set_full_screen_effect(self.engine.horizontal_wipe_effect, [HorizontalWipeDirection.RIGHT])
            self.engine.start_full_screen_effect()

        elif new_state == PurgeSectionStates.GAME_TRANSITION:
            self.member_dialog.reset_talking()
            self.pride_dialog.reset_talking()

            effect_image = self.prepare_member_effect()
            self.member_move_effect.set_tiles(effect_image.tiles)
            self.member_move_effect.start([HorizontalMoveDirection.OUT_LEFT])

    def open_instructions(self):
        self.pre_instructions_state = self.state
        self.seen_instructions = True
        self.ui.instructions_close_button.enable()
        self.ui.instructions_open_button.disable()
        self.ui.roll_button.disable()
        self.change_state(PurgeSectionStates.INSTRUCTION)

    def close_instructions(self):
        self.ui.instructions_close_button.disable()
        self.ui.instructions_open_button.enable()
        self.ui.roll_button.enable()
        self.change_state(self.pre_instructions_state)
        self.pre_instructions_state = None

    def render_instructions(self, console):
        self.draw_image(console, purge_section_info["instructions_image"].rect, purge_section_info["instructions_image"].image)
        self.draw_button(console, purge_section_info["instructions_close_button"])

    def should_render_pride(self):
        return self.state == PurgeSectionStates.GAME_SETUP or self.state == PurgeSectionStates.GAME_MEMBER_DIALOG or self.state == PurgeSectionStates.GAME or self.state == PurgeSectionStates.GAME_TRANSITION or self.state == PurgeSectionStates.GAME_PRIDE_DIALOG or self.state == PurgeSectionStates.INSTRUCTION

    def should_render_pride_dialog(self):
        return self.pride_dialog.is_talking() or self.pride_dialog.is_finished()

    def start_pride_talking(self, text):
        self.pride_dialog.start_talking(text)
        self.pride_mouth_animaton.start()

    def should_render_member(self):
        return self.state == PurgeSectionStates.GAME_MEMBER_DIALOG or self.state == PurgeSectionStates.GAME or self.state == PurgeSectionStates.GAME_PRIDE_DIALOG or self.state == PurgeSectionStates.INSTRUCTION

    def should_render_member_dialog(self):
        return self.member_dialog.is_talking() or self.member_dialog.is_finished()

    def start_member_talking(self, text):
        self.member_dialog.start_talking(text)
        self.member_mouth_animaton.start()

    def start_pride_talking(self, text):
        self.pride_dialog.start_talking(text)
        self.pride_mouth_animaton.start()

    def pick_member(self):
        self.current_member = 0

    def prepare_pride_effect(self):
        pride_rect = purge_section_info["pride_character"].rect
        pride_image = purge_section_info["pride_character"].image

        eyes_rect = purge_section_info["pride_eyes_open"].rect
        eyes_image = self.pride_eyes_animaton.get_current_frame()

        mouth_rect = purge_section_info["pride_mouth_open"].rect
        mouth_image = self.pride_mouth_animaton.get_current_frame()

        self.pride_move_effect = HorizontalMoveEffect(self.engine, pride_rect.x,pride_rect.y,pride_rect.width,pride_rect.height)

        temp_console = tcod.Console(width=self.pride_move_effect.width, height=self.pride_move_effect.height, order="F")
        temp_console.tiles_rgb[0: pride_rect.width,0:  pride_rect.height] = pride_image.tiles[0: pride_rect.width, 0: pride_rect.height]["graphic"]
        temp_console.tiles_rgb[4: 4+eyes_rect.width,3:  3+eyes_rect.height] = eyes_image.tiles[0: eyes_rect.width, 0: eyes_rect.height]["graphic"]
        temp_console.tiles_rgb[5: 5+mouth_rect.width,6:  6+mouth_rect.height] = mouth_image.tiles[0: mouth_rect.width, 0: mouth_rect.height]["graphic"]

        return temp_console

    def prepare_member_effect(self):
        member = members[self.current_member]

        member_rect = purge_section_info["member_"+str(member.id)+"_character"].rect
        member_image = purge_section_info["member_"+str(member.id)+"_character"].image

        eyes_rect = purge_section_info["member_animation_rects"][self.member_eyes_animaton.get_current_frame()]
        eyes_image = purge_section_info["member_"+str(member.id)+"_frames"]["eo"]

        mouth_rect = purge_section_info["member_animation_rects"][self.member_mouth_animaton.get_current_frame()]
        mouth_image = purge_section_info["member_"+str(member.id)+"_frames"]["mc"]

        self.member_move_effect = HorizontalMoveEffect(self.engine, member_rect.x,member_rect.y,member_rect.width,member_rect.height)

        temp_console = tcod.Console(width=self.member_move_effect.width, height=self.member_move_effect.height, order="F")
        temp_console.tiles_rgb[0: member_rect.width,0:  member_rect.height] = member_image.tiles[0: member_rect.width, 0: member_rect.height]["graphic"]
        temp_console.tiles_rgb[4: 4+eyes_rect.width,3:  3+eyes_rect.height] = eyes_image.tiles[0: eyes_rect.width, 0: eyes_rect.height]["graphic"]
        temp_console.tiles_rgb[5: 5+mouth_rect.width,6:  6+mouth_rect.height] = mouth_image.tiles[0: mouth_rect.width, 0: mouth_rect.height]["graphic"]

        return temp_console

    def bar_member(self):
        self.barred_members += 1
        self.start_pride_talking("Get out of here you presbyterian bastard!")
        self.change_state(PurgeSectionStates.GAME_PRIDE_DIALOG)

    def pass_member(self):
        self.passed_members += 1
        self.start_pride_talking("Come on in, fellow lover of liberty!")
        self.change_state(PurgeSectionStates.GAME_PRIDE_DIALOG)