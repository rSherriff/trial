from actions.actions import EscapeAction
from ui.ui import UI, Button
from sections.section_layouts import title_section_info
from actions.game_actions import JumpToStageAction


class TitleUI(UI):
    def __init__(self, section, tiles):
        super().__init__(section)

    def setup_buttons(self, stage):
        bs = title_section_info["start_button"]
        self.start_button = Button(bs.x,bs.y,bs.width,bs.height, click_action=JumpToStageAction(self.section.engine, stage), h_fg=bs.h_fg)
        self.elements.append(self.start_button)

"""
        bd = [21, 20, 9, 3]  # Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        self.start_button = Button(x=bd[0], y=bd[1], width=bd[2],height=bd[3], click_action=EnterOptionsAction(self.section.engine), tiles=button_tiles, normal_bg=(191,191,191), highlight_bg=(128,128,128))
        self.elements.append(self.start_button)

        bd = [21, 24, 9, 3]  # Button Dimensions
        button_tiles = tiles[bd[0]:bd[0] + bd[2], bd[1]:bd[1] + bd[3]]
        self.quit_button = Button(x=bd[0], y=bd[1], width=bd[2],height=bd[3], click_action=EscapeAction(self.section.engine), tiles=button_tiles, normal_bg=(191,191,191), highlight_bg=(128,128,128))
        self.elements.append(self.quit_button)
"""
        