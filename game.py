import json
from collections import OrderedDict
from datetime import date, datetime, timedelta
from enum import Enum, auto
from threading import Timer

from pygame import mixer

from actions.actions import OpenNotificationDialog

from effects.horizontal_wipe_effect import (HorizontalWipeDirection,
                                            HorizontalWipeEffect)
from effects.melt_effect import MeltWipeEffect, MeltWipeEffectType
from engine import CONFIRMATION_DIALOG, NOTIFICATION_DIALOG, Engine, GameState
from sections.confirmation import Confirmation
from sections.intro_section import IntroSection
from sections.notification import Notification
from sections.menu_section import MenuSection
from sections.hunt_section import HuntSection
from sections.title_section import TitleSection


INTRO_SECTION = "introSection"
MENU_SECTION = "menuSection"
HUNT_SECTION = "huntSection"
TITLE_SECTION = "titleSection"

class Game(Engine):
    def __init__(self, teminal_width: int, terminal_height: int):
        super().__init__(teminal_width, terminal_height)

        self.setup_effects()
        self.start_game()

    def start_game(self):
        pass

    def create_new_save_data(self):
        pass

    def load_initial_data(self, data):
        pass

    def load_fonts(self):
        pass

    #*********************************************
    # Effects
    #*********************************************

    def setup_effects(self):
        super().setup_effects()
        self.intro_end_effect = MeltWipeEffect(self, 0, 0, self.screen_width, self.screen_height, MeltWipeEffectType.RANDOM, 20)
        self.start_stage_effect = MeltWipeEffect(self, 0, 0, self.screen_width, self.screen_height, MeltWipeEffectType.RANDOM, 20)

    #*********************************************
    # Sections
    #*********************************************

    def setup_sections(self):
        self.disabled_sections = []
        self.disabled_ui_sections = []

        self.intro_sections = OrderedDict()
        self.intro_sections[INTRO_SECTION] = IntroSection(self,0,0,self.screen_width, self.screen_height, INTRO_SECTION)

        self.menu_sections = OrderedDict()
        self.menu_sections[MENU_SECTION] = MenuSection(self,0,0,self.screen_width, self.screen_height, MENU_SECTION)

        self.game_sections = OrderedDict()
        self.game_sections[HUNT_SECTION] = HuntSection(self,0,0,self.screen_width, self.screen_height, HUNT_SECTION)
        self.game_sections[TITLE_SECTION] = TitleSection(self,0,0,self.screen_width, self.screen_height, TITLE_SECTION)
  
        self.misc_sections = OrderedDict()
        self.misc_sections[NOTIFICATION_DIALOG] = Notification(self, 0,0, self.screen_width, self.screen_height, NOTIFICATION_DIALOG)
        self.misc_sections[CONFIRMATION_DIALOG] = Confirmation(self, 0,0, self.screen_width, self.screen_height, CONFIRMATION_DIALOG)

        self.completion_sections = OrderedDict()

        self.disabled_sections = [CONFIRMATION_DIALOG, NOTIFICATION_DIALOG]
        self.disabled_ui_sections = [CONFIRMATION_DIALOG, NOTIFICATION_DIALOG]

    def refresh_open_sections(self):
        for key, section in self.get_active_sections():
            section.refresh()

    def end_intro(self):
        super().end_intro()
        self.set_full_screen_effect(self.intro_end_effect)
        self.start_full_screen_effect()

    def close_all_game_sections(self):
        self.disable_section(self.game_sections[HUNT_SECTION])
        self.disable_section(self.game_sections[TITLE_SECTION])
        
        self.game_sections[HUNT_SECTION].close()
        self.game_sections[TITLE_SECTION].close()

    def start_stage(self, stage):
        self.state = GameState.IN_GAME

        self.close_all_game_sections()

        self.enable_section(stage)
        self.game_sections[stage].open()

        self.set_full_screen_effect(self.start_stage_effect)
        self.start_full_screen_effect()
