from actions.actions import EscapeAction
from ui.ui import UI, Button
from sections.section_layouts import hunt_section_info
from actions.game_actions import JumpToMenuAction, GenericAction


class HuntUI(UI):
    def __init__(self, section, tiles):
        super().__init__(section)

    def setup_buttons(self):
        bs = hunt_section_info["quit_button"]
        self.quit_button = Button(bs.x,bs.y,bs.width,bs.height, click_action=JumpToMenuAction(self.section.engine), h_fg=bs.h_fg)
        self.elements.append(self.quit_button)

        bs = hunt_section_info["instructions_button"]
        self.instructions_button = Button(bs.x,bs.y,bs.width,bs.height, click_action=GenericAction(self.section.engine, self.section.open_instructions), h_fg=bs.h_fg)
        self.elements.append(self.instructions_button)

"""
        bd = [21, 24, 9, 3]  # Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        self.quit_button = Button(x=bd[0], y=bd[1], width=bd[2],height=bd[3], click_action=EscapeAction(self.section.engine), tiles=button_tiles, normal_bg=(191,191,191), highlight_bg=(128,128,128))
        self.elements.append(self.quit_button)
"""
        