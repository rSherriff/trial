
import copy
import json
from enum import Enum, auto
from math import sqrt

import numpy as np
import tcod
from tcod import Console

from actions.actions import EscapeAction
from animation import Animation
from effects.horizontal_wipe_effect import (HorizontalWipeDirection,
                                            HorizontalWipeEffect)
from sections.section import Section
from sections.section_layouts import menu_section_layout
from ui.menu_ui import MenuUI
from image import Image


class MenuState(Enum):
    MAIN = auto()
    STAGE_SCREEN = auto()
    OPTIONS = auto()


class MenuSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name:str) -> None:
        super().__init__(engine, x, y, width, height, "", name)      
        self.ui = MenuUI(self, self.tiles["graphic"])
        self.main_tiles = self.load_xp_data("main_menu.xp")
        self.load_tiles("main", self.main_tiles)
        self.transition_effect = HorizontalWipeEffect(self.engine,0,0,self.width, self.height)

        frames = {"o":Image.from_rect(menu_section_layout["charles_frame_one"], "images/menu_charles.xp"),"-":Image.from_rect(menu_section_layout["charles_frame_two"], "images/menu_charles.xp")}
        timeline = "oooooooooooooo-ooooooooo-oooooooo-ooooooooooooo-ooooooooooooooooo-o-oo"
        self.charles_animation = Animation(self.engine, frames, timeline, 0.1)
        self.charles_animation.start()
        
    def update(self):
        pass
    
    def render(self, console):
        super().render(console)
        self.draw_button(console, menu_section_layout["start_button"])
        self.draw_image(console, menu_section_layout["charles_rect"], self.charles_animation.get_current_frame())
        self.render_ui(console)

    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass
