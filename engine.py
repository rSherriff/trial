from __future__ import annotations

import abc
import json
import os
import random
from collections import OrderedDict
from enum import Enum, auto

import tcod
from pygame import mixer
from tcod.console import Console

from actions.actions import OpenNotificationDialog
from application_path import get_app_path
from effects.melt_effect import MeltWipeEffect, MeltWipeEffectType
from fonts.font_manager import FontManager
from input_handlers import EventHandler, MainGameEventHandler
from sections.confirmation import Confirmation
from sections.intro_section import IntroSection
from sections.notification import Notification
from utils.delta_time import DeltaTime
from game_data.game_structure import intro_splashes


class GameState(Enum):
    INTRO = auto()
    MENU = auto()
    IN_GAME = auto()

NOTIFICATION_DIALOG = "notificationDialog"
CONFIRMATION_DIALOG = "confirmationDialog"

class Engine(abc.ABC):
    def __init__(self, teminal_width: int, terminal_height: int):

        mixer.init()

        self.save_data = None
        if os.path.isfile("game_data/game_save.json"):
            with open("game_data/game_save.json") as f:
                self.save_data = json.load(f)
                self.set_mixer_volume(self.save_data["volume"])
        else:
            self.create_new_save_data()

        self.screen_width = teminal_width
        self.screen_height = terminal_height
        self.delta_time = DeltaTime()

        self.player = None

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.sections_disabled_by_dialog = {}

        self.setup_effects()
        self.setup_sections()

        self.tick_length = 2
        self.time_since_last_tick = -2

        self.state = GameState.INTRO

        self.font_manager = FontManager()
        self.load_fonts()

        self.in_stage_music_queue = False
        self.playing_menu_music = False
        
        self.intro_sections["introSection"].load_splashes(intro_splashes)
            
    def create_new_save_data(self):
        self.save_data = dict()
        self.save_data["fullscreen"] = True
        self.save_data["volume"] = 0.5
        self.set_mixer_volume(self.save_data["volume"])

    @abc.abstractmethod
    def load_initial_data(self, data):
        pass

    @abc.abstractmethod
    def load_fonts(self):
        pass

    def render(self, root_console: Console) -> None:
        """ Renders the game to console """
        for section_key, section_value in self.get_active_sections():
            if section_key not in self.disabled_sections:
                section_value.render(root_console)

        if self.full_screen_effect != None and self.full_screen_effect.in_effect == True:
            self.full_screen_effect.render(root_console)
        else:
            self.last_rendered_frame_tiles = root_console.tiles_rgb

        #root_console.print(40, 1, str(self.mouse_location), (255,255,255))

    def update(self):
        """ Engine update tick """
        for _, section in self.get_active_sections():
            section.update()

        self.delta_time.update_delta_time()

        if self.is_in_game():
            self.time_since_last_tick += self.get_delta_time()

            self.tick_length -= 0.0002
            if self.time_since_last_tick > self.tick_length and self.state == self.is_in_game():
                self.time_since_last_tick = 0

        if self.in_stage_music_queue and not mixer.music.get_busy():
            self.advance_music_queue()

    def late_update(self):
       for _, section in self.get_active_sections():
            section.late_update()

    def is_in_game(self):
        return self.state == GameState.IN_GAME

    def handle_events(self, context: tcod.context.Context):
        self.event_handler.handle_events(context, discard_events=self.is_ui_paused())

    def setup_effects(self):
        self.full_screen_effect = None

    def set_full_screen_effect(self, effect, parameters=None):
        self.full_screen_effect = effect
        self.full_screen_effect_parameters = parameters
        self.full_screen_effect.set_tiles(self.last_rendered_frame_tiles)

    def start_full_screen_effect(self):
        self.full_screen_effect.start(self.full_screen_effect_parameters)

    @abc.abstractmethod
    def setup_sections(self): 
        pass

    def get_active_sections(self):
        sections = OrderedDict()
        if self.state == GameState.INTRO:
            sections = dict(filter(lambda elem: elem[0] not in self.disabled_sections, self.intro_sections.items()))
        elif self.state == GameState.MENU:
            sections = dict(filter(lambda elem: elem[0] not in self.disabled_sections, self.menu_sections.items()))
        elif self.is_in_game():
            sections = dict(filter(lambda elem: elem[0] not in self.disabled_sections, self.game_sections.items()))

        sections |= self.misc_sections
        return sections.items()

    def get_active_ui_sections(self):
        sections = OrderedDict()
        if self.state == GameState.INTRO:
            sections = dict(filter(lambda elem: elem[0] not in self.disabled_ui_sections, self.intro_sections.items()))
        elif self.state == GameState.MENU:
            sections =  dict(filter(lambda elem: elem[0] not in self.disabled_ui_sections, self.menu_sections.items()))
        elif self.is_in_game():
            sections =  dict(filter(lambda elem: elem[0] not in self.disabled_ui_sections, self.game_sections.items()))

        sections |= (dict(filter(lambda elem: elem[0] not in self.disabled_ui_sections, self.misc_sections.items())))
        return sections.items()

    def enable_section(self, section):
        if section in self.disabled_sections:
            self.disabled_sections.remove(section)
            self.enable_ui_section(section)

    def disable_section(self, section):
        if section not in self.disabled_sections:
            self.disabled_sections.append(section)
            self.disable_ui_section(section)

    def enable_ui_section(self, section):
        if section in self.disabled_ui_sections:
            self.disabled_ui_sections.remove(section)

    def disable_ui_section(self, section):
        if section not in self.disabled_ui_sections:
            self.disabled_ui_sections.append(section)

    def disable_all_ui_sections(self, sections_to_exclude):
        sections_disabled = []
        for section, _ in self.get_active_ui_sections():
            if section not in sections_to_exclude and section not in self.disabled_ui_sections:
                self.disable_ui_section(section) 
                sections_disabled.append(section)
        return sections_disabled

    def enable_ui_sections(self, sections):
        for section in sections:
            self.enable_ui_section(section)

    def is_section_disabled(self, section):
        return section in self.disabled_sections

    def queue_music(self, stage):
        music = self.stage_music[stage]["music"]
        volume = self.stage_music[stage]["music_volume"]
        if len(music) > 0:
            random.shuffle(music)
            mixer.music.set_volume(self.save_data["volume"])
            self.current_music_index = 0
            self.music_queue = music
            self.advance_music_queue()
            self.in_stage_music_queue = True
        
    def advance_music_queue(self):
        print("Playing: " + self.music_queue[self.current_music_index])
        mixer.music.load("sounds/music/" + self.music_queue[self.current_music_index])
        self.current_music_index += 1

        if self.current_music_index >= len(self.music_queue):
            self.current_music_index = 0

        self.play_music()

    def play_music(self):
        mixer.music.play()

    def end_music_queue(self, fadeout_time):
        mixer.music.fadeout(fadeout_time)
        self.in_stage_music_queue = False

    def play_music_file(self, file):
        if not self.in_stage_music_queue and os.path.isfile("sounds/music/" + file):
            mixer.music.load("sounds/music/" + file)
            mixer.music.play()
        else:
            print("Tried to play music that doesn't exist!  " + file)

    def play_menu_music(self, file=""):
        if len(file) > 0:
            self.menu_music = file
        if os.path.isfile("sounds/music/" + self.menu_music):
            mixer.music.load("sounds/music/" + self.menu_music)
            mixer.music.play()
        else:
            print("Tried to play music that doesn't exist!  " + self.menu_music)


    def open_menu(self):
        self.change_state(GameState.MENU)
        self.full_screen_effect.start()

    def change_state(self, new_state):
        old_state = self.state

        self.state = new_state
   
    def get_delta_time(self):
        return self.delta_time.get_delta_time()

    def quit(self):
        raise SystemExit()

    def toggle_fullscreen(self):
        with open("game_data/game_save.json", "w") as f:
            self.save_data["fullscreen"] = not self.save_data["fullscreen"]
            json.dump(self.save_data, f, indent=2)

        OpenNotificationDialog(self, "The game must be restarted for this option to take effect.", "Menu").perform()
            
    def open_confirmation_dialog(self, text, confirmation_action, section, enable_ui_on_confirm):
        self.misc_sections[CONFIRMATION_DIALOG].setup(text, confirmation_action, section, enable_ui_on_confirm)
        self.enable_section(CONFIRMATION_DIALOG)
        self.sections_disabled_by_dialog[CONFIRMATION_DIALOG] = self.disable_all_ui_sections([CONFIRMATION_DIALOG])

    def close_confirmation_dialog(self, section, enable_ui):
        self.disable_section(CONFIRMATION_DIALOG)

        self.enable_ui_sections(self.sections_disabled_by_dialog[CONFIRMATION_DIALOG])
        if not enable_ui:
            self.disable_ui_section(section)

    def is_confirmation_dialog_open(self):
        return CONFIRMATION_DIALOG not in self.disabled_sections

    def open_notification_dialog(self, text, section):
        self.misc_sections[NOTIFICATION_DIALOG].setup(text, section)
        self.enable_section(NOTIFICATION_DIALOG)
        self.sections_disabled_by_dialog[NOTIFICATION_DIALOG] = self.disable_all_ui_sections([NOTIFICATION_DIALOG])

    def close_notification_dialog(self, section):
        self.disable_section(NOTIFICATION_DIALOG)
        self.enable_ui_sections(self.sections_disabled_by_dialog[NOTIFICATION_DIALOG])

    def is_ui_paused(self):
        if self.full_screen_effect == None:
            return False
        else:   
            return self.full_screen_effect.in_effect == True

    def end_intro(self):
        self.change_state(GameState.MENU)

    def set_mixer_volume(self, volume):
        mixer.music.set_volume(volume)
        with open("game_data/game_save.json", "w") as f:
            self.save_data["volume"] = volume
            json.dump(self.save_data, f, indent=2)
