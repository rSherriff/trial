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
    INSTRUCTION = auto(),
    

class PurgeSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "purge_section.xp", name) 
        self.ui = PurgeUI(self, self.tiles["graphic"])     
        self.seen_instructions = False

    def update(self):
        super().update()

        self.time_into_state += self.engine.get_delta_time()
    
    def render(self, console):
        super().render(console)

        if self.state == PurgeSectionStates.INSTRUCTION:
            self.render_instructions(console)

        self.draw_button(console, purge_section_info["instructions_open_button"])
        self.draw_button(console, purge_section_info["pass_button"])
        self.draw_button(console, purge_section_info["bar_button"])
        self.draw_button(console, purge_section_info["roll_button"])
        self.render_ui(console)

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
