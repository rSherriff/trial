
import copy
import json
from enum import Enum, auto
from math import sqrt

import numpy as np
import tcod
from tcod import Console

from actions.actions import EscapeAction
from effects.horizontal_wipe_effect import (HorizontalWipeDirection,
                                            HorizontalWipeEffect)
from sections.section import Section
from sections.section_layouts import ButtonStruct, menu_section_layout
from ui.menu_ui import MenuUI


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
        
    def update(self):
        pass
    
    def render(self, console):
        super().render(console)
        self.draw_button(console, menu_section_layout["start_button"])
        self.render_ui(console)
        
    def draw_button(self, console, bs):
        console.draw_frame(bs.x,bs.y,bs.width,bs.height, decoration=bs.decoration, bg=bs.bg, fg=bs.fg)
        console.print_box(bs.x+1,bs.y+1,bs.width-2,bs.height-2,string=bs.text,alignment=tcod.CENTER, bg=bs.font_bg, fg=bs.font_fg)



    def mousedown(self,button,x,y):
        pass

    def keydown(self, key):
        pass
