from enum import Enum, auto

import tcod

from animation import Animation
from dialog import Dialog
from effects.horizontal_wipe_effect import HorizontalWipeDirection
from game_data.game_structure import chapters
from sections.section import Section
from sections.section_layouts import Rect, ImageRect, hunt_section_info, land_green, main_text
from ui.hunt_ui import HuntUI
from typing import NamedTuple
from image import Image
from actions.game_actions import EndCurrentChapterAction


class HuntSectionStates(Enum):
    NONE = auto(),
    PENDING = auto(),
    INTRO = auto(),
    INSTRUCTION = auto(),
    GAME_SETUP = auto(),
    GAME = auto(),
    GAME_RESET = auto(),
    GAME_TRANSITION = auto(),
    GAME_TEARDOWN = auto(),

class HuntGameNodeTypes(Enum):
    CHASED = auto()
    PURSUER = auto()
    GOAL = auto()

class HuntGameNode(NamedTuple):
    type: int
    effects : list

class HuntGame(NamedTuple):
    x : int
    y : int
    width: int
    height: int
    grid : ImageRect
    nodes : list
    start_nodes : tuple

class HuntGameConstants(NamedTuple):
    x_step: int
    y_step: int
    chased_chr: int
    pursuer_chr: int
    goal_chr: int

    
GAME_1_NODES = ((HuntGameNode(HuntGameNodeTypes.CHASED,[(1,2),(0,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,1),(2,0)]),HuntGameNode(HuntGameNodeTypes.PURSUER,[])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(0,0),(0,1)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(0,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,0),(1,1)])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(2,1)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,2),(2,2)]),HuntGameNode(HuntGameNodeTypes.GOAL,[])))

GAME_1 = HuntGame(x=34, y=15, width=3, height=3, grid=hunt_section_info["game_grid_3x3"], nodes=GAME_1_NODES, start_nodes=[(0,1)])

GAME_2_NODES = ((HuntGameNode(HuntGameNodeTypes.CHASED,[(2,1),(3,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(2,3),(3,3)]),HuntGameNode(HuntGameNodeTypes.GOAL,[]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,3),(3,2)])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(0,1),(3,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(2,0),(2,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,3),(2,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(1,1)])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(3,1),(3,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,0),(3,0)]),HuntGameNode(HuntGameNodeTypes.PURSUER,[]),HuntGameNode(HuntGameNodeTypes.PURSUER,[])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(3,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,0),(0,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(2,2),(3,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(1,2)])))

GAME_2 = HuntGame(x=32, y=13, width=4, height=4, grid=hunt_section_info["game_grid_4x4"], nodes=GAME_2_NODES, start_nodes=[(3,3)])

GAME_3_NODES = ((HuntGameNode(HuntGameNodeTypes.CHASED,[(4,0),(4,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,0),(0,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(2,2),(2,4)]),HuntGameNode(HuntGameNodeTypes.PURSUER,[]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,3),(4,0)])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(0,4),(2,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(3,0),(1,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,4),(2,1)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(3,0),(4,0)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(3,0),(2,3)])),
                (HuntGameNode(HuntGameNodeTypes.PURSUER,[]),HuntGameNode(HuntGameNodeTypes.PURSUER,[]),HuntGameNode(HuntGameNodeTypes.CHASED,[(1,2),(0,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,0),(2,0)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,2),(1,2)])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(1,1),(0,4)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,3),(4,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(4,1),(4,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(4,1),(0,3)]),HuntGameNode(HuntGameNodeTypes.CHASED,[])),
                (HuntGameNode(HuntGameNodeTypes.CHASED,[(3,0),(2,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(0,1),(2,2)]),HuntGameNode(HuntGameNodeTypes.CHASED,[(4,1),(0,3)]),HuntGameNode(HuntGameNodeTypes.GOAL,[]),HuntGameNode(HuntGameNodeTypes.CHASED,[(3,1),(3,3)])))

GAME_3 = HuntGame(x=30, y=11, width=5, height=5, grid=hunt_section_info["game_grid_5x5"], nodes=GAME_3_NODES, start_nodes=[(1,3)])

HUNT_GAME_CONSTANTS = HuntGameConstants(x_step= 2, y_step= 2,chased_chr= chr(249), pursuer_chr= chr(214), goal_chr= chr(163))

class HuntSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, name: str = ""):
        super().__init__(engine, x, y, width, height, "hunt_section.xp", name) 
        self.ui = HuntUI(self, self.tiles["graphic"])     

        self.advisor_dialog = Dialog(self, hunt_section_info["advisor_dialog_rect"], hunt_section_info["advisor_dialog_text_color"], hunt_section_info["advisor_dialog_fg"])
        self.state = HuntSectionStates.NONE
        self.time_into_state = 0

        frames = {"o":hunt_section_info["advisor_top_eyes_open"].image,"-":hunt_section_info["advisor_top_eyes_closed"].image}
        timeline = "oooooooooooooo-ooooooooo-oooooooo-ooooooooooooo-ooooooooooooooooo-o-oo"
        self.advisor_top_animaton = Animation(self.engine, frames, timeline, 0.1)
        self.advisor_top_animaton.start()

        frames = {"o":hunt_section_info["advisor_btm_mouth_closed"].image,"-":hunt_section_info["advisor_btm_mouth_open"].image}
        timeline = "o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-"
        self.advisor_btm_animaton = Animation(self.engine, frames, timeline, 0.1)

        self.seen_instructions = False
        self.current_game = 0
        self.games = [GAME_1, GAME_2, GAME_3]
        self.last_activated_node = None

    def update(self):
        super().update()

        self.time_into_state += self.engine.get_delta_time()

        if self.state == HuntSectionStates.PENDING:
            if self.time_into_state >= hunt_section_info["start_wait_time"]:
                self.change_state(HuntSectionStates.INTRO)

        elif self.state == HuntSectionStates.INTRO:
            self.update_dialog()

        elif self.state == HuntSectionStates.GAME_SETUP:
            if self.time_into_state >= hunt_section_info["setup_wait_time"]:
                self.change_state(HuntSectionStates.GAME)

        elif self.state == HuntSectionStates.GAME:
            if not self.seen_instructions and self.time_into_state >= hunt_section_info["see_instructions_wait_time"]:
                self.open_instructions()
                return

            game = self.games[self.current_game]
                
            if not self.last_activated_node == None:
                node = game.nodes[self.last_activated_node[0]][self.last_activated_node[1]]
                if node.type == HuntGameNodeTypes.PURSUER:
                    self.change_state(HuntSectionStates.GAME_RESET)
                elif node.type == HuntGameNodeTypes.GOAL:
                    self.change_state(HuntSectionStates.GAME_TRANSITION)

        elif self.state == HuntSectionStates.GAME_RESET:
            self.update_dialog()

        elif self.state == HuntSectionStates.GAME_TRANSITION:
            self.update_dialog()

        elif self.state == HuntSectionStates.GAME_TEARDOWN:
            self.update_dialog()

    def update_dialog(self):
        self.advisor_dialog.update()
        if self.advisor_dialog.is_finished():
            self.advisor_btm_animaton.stop()
    
    def render(self, console):
        super().render(console)

        self.render_advisor_dialog(console)
        self.render_advisor(console)  
        self.render_game_grid(console)   
        self.render_special_nodes(console)   

        if self.state == HuntSectionStates.INSTRUCTION:
            self.render_instructions(console)
        elif self.state == HuntSectionStates.GAME:
            self.render_normal_nodes(console)

            if self.seen_instructions:
                self.draw_button(console, hunt_section_info["instructions_open_button"])

        self.draw_button(console, hunt_section_info["quit_button"])
        self.render_ui(console)

    def render_advisor_dialog(self, console):
        if self.should_render_dialog():
            self.draw_image(console, hunt_section_info["speech_mark_image"].rect, hunt_section_info["speech_mark_image"].image)

            box_rect = hunt_section_info["advisor_dialog_rect"]
            dialog_box_rect = Rect(box_rect.x, box_rect.y,  max(box_rect.width, self.advisor_dialog.longest_line), max(4,self.advisor_dialog.get_current_height()))
            self.draw_box(console, dialog_box_rect, hunt_section_info["advisor_dialog_decoration"],hunt_section_info["advisor_dialog_margin"], hunt_section_info["advisor_dialog_fg"],hunt_section_info["advisor_dialog_bg"])

            self.advisor_dialog.render(console)

    def render_game_grid(self, console):
        if self.should_render_game_grid():
            self.draw_image(console, self.games[self.current_game].grid.rect, self.games[self.current_game].grid.image)

    def render_normal_nodes(self, console):
        for node_pos in self.get_currently_active_nodes():
            x ,y = self.get_node_coordinates(node_pos)
            console.print(x,y,HUNT_GAME_CONSTANTS.chased_chr,fg=main_text,bg=land_green)

    def render_special_nodes(self,console):
        if self.should_render_special_nodes():
            game = self.games[self.current_game]
            if not self.last_activated_node == None:
                node_pos = self.last_activated_node
                x ,y = self.get_node_coordinates(node_pos)
                node = game.nodes[node_pos[0]][node_pos[1]]

                if node.type == HuntGameNodeTypes.PURSUER:
                    console.print(x,y,HUNT_GAME_CONSTANTS.pursuer_chr,fg=main_text,bg=land_green)
                elif node.type == HuntGameNodeTypes.GOAL:
                    console.print(x,y,HUNT_GAME_CONSTANTS.goal_chr,fg=main_text,bg=land_green)

    def render_advisor(self, console):
        self.draw_image(console, hunt_section_info["advisor_top_eyes_open"].rect, self.advisor_top_animaton.get_current_frame())
        if self.advisor_dialog.is_talking():
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_open"].rect, self.advisor_btm_animaton.get_current_frame())
        else:
            self.draw_image(console, hunt_section_info["advisor_btm_mouth_closed"].rect, hunt_section_info["advisor_btm_mouth_closed"].image)

    def render_instructions(self, console):
        self.draw_image(console, hunt_section_info["instructions_image"].rect, hunt_section_info["instructions_image"].image)
        self.draw_button(console, hunt_section_info["instructions_close_button"])

    def open(self):
        self.ui.setup_buttons()
        self.change_state(HuntSectionStates.PENDING)        

    def refresh(self):
        pass

    def close(self):
        pass
      
    def mousedown(self,button,x,y):
        if self.state == HuntSectionStates.INTRO:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            else:
                self.change_state(HuntSectionStates.GAME_SETUP)
        elif self.state == HuntSectionStates.GAME:
            if button == 1:
                game = self.games[self.current_game]
                x = (x-game.x)/HUNT_GAME_CONSTANTS.x_step
                y = (y-game.y)/HUNT_GAME_CONSTANTS.y_step
                if x.is_integer() and y.is_integer():
                    x = int(x)
                    y = int(y)
                    if x < game.width and y < game.height:
                        for i in self.get_currently_active_nodes():
                            if (y,x) == i:
                                self.last_activated_node = (y,x)
        elif self.state == HuntSectionStates.GAME_RESET or self.state == HuntSectionStates.GAME_TRANSITION:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            else:
                self.change_state(HuntSectionStates.GAME_SETUP)
        elif self.state == HuntSectionStates.GAME_TEARDOWN:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            else:
                self.end_chapter()

    def keydown(self, key):
        if key == tcod.event.K_ESCAPE or key == tcod.event.K_SPACE or key == tcod.event.K_RETURN:
            if self.advisor_dialog.is_talking():
                self.advisor_dialog.end_talking()
            elif self.state == HuntSectionStates.INTRO:
                self.change_state(HuntSectionStates.GAME_SETUP)
            elif self.state == HuntSectionStates.INSTRUCTION:
                self.change_state(HuntSectionStates.GAME)

        if key == tcod.event.K_q:
            self.end_chapter()

    def change_state(self, new_state):
        print("Changing to state:", new_state)

        old_state = self.state
        if old_state == HuntSectionStates.GAME_TRANSITION:
            if self.current_game < len(self.games) - 1:
                self.current_game += 1

        self.state = new_state
        self.time_into_state = 0

        if new_state == HuntSectionStates.PENDING:
            self.ui.instructions_open_button.disable()
            self.ui.instructions_close_button.disable()
        elif new_state == HuntSectionStates.INTRO:
            self.advisor_dialog.start_talking(chapters["hunt"]["intro"])
            self.ui.instructions_open_button.disable()
            self.advisor_btm_animaton.start()
        elif new_state == HuntSectionStates.INSTRUCTION:
            self.ui.instructions_open_button.disable()
            self.ui.instructions_close_button.enable()
            self.ui.quit_button.disable()
        elif new_state == HuntSectionStates.GAME_RESET:
            self.advisor_dialog.start_talking("Can I get this going so it changes state on dialog end after a click?")
            self.ui.instructions_open_button.disable()
            self.advisor_btm_animaton.start()
        elif new_state == HuntSectionStates.GAME_TRANSITION:

            if self.current_game < len(self.games) - 1:
                self.advisor_dialog.start_talking("Can I get this going so it changes state on dialog end after a click?")
                self.ui.instructions_open_button.disable()
                self.advisor_btm_animaton.start()
            else:
                self.change_state(HuntSectionStates.GAME_TEARDOWN)
            
        elif new_state == HuntSectionStates.GAME:
            self.reset_game()
            self.advisor_dialog.reset_talking()
            self.ui.instructions_open_button.enable()
            self.ui.instructions_close_button.disable()
            self.ui.quit_button.enable()
        elif new_state == HuntSectionStates.GAME_TEARDOWN:
            self.ui.instructions_open_button.disable()
            self.advisor_dialog.start_talking("Section finished!")

        self.engine.set_full_screen_effect(self.engine.horizontal_wipe_effect, [HorizontalWipeDirection.RIGHT])
        self.engine.start_full_screen_effect()

    def open_instructions(self):
        self.pre_instructions_state = self.state
        self.seen_instructions = True
        self.change_state(HuntSectionStates.INSTRUCTION)

    def close_instructions(self):
        self.change_state(self.pre_instructions_state)
        self.pre_instructions_state = None

    def reset_game(self):
        self.last_activated_node = None

    def get_currently_active_nodes(self):
        game = self.games[self.current_game]
        if self.last_activated_node == None:
            return game.start_nodes
        else:
            x = self.last_activated_node[0]
            y = self.last_activated_node[1]
            return game.nodes[x][y].effects

    def should_render_dialog(self):
        return self.state == HuntSectionStates.INTRO or self.state == HuntSectionStates.GAME_RESET or self.state == HuntSectionStates.GAME_TRANSITION or self.state == HuntSectionStates.GAME_TEARDOWN

    def should_render_game_grid(self):
        return self.state == HuntSectionStates.GAME or self.state == HuntSectionStates.GAME_RESET or self.state == HuntSectionStates.GAME_SETUP or self.state == HuntSectionStates.GAME_TRANSITION or self.state == HuntSectionStates.GAME_TEARDOWN
    
    def should_render_special_nodes(self):
        return self.state == HuntSectionStates.GAME or self.state == HuntSectionStates.GAME_RESET or self.state == HuntSectionStates.GAME_TRANSITION or self.state == HuntSectionStates.GAME_TEARDOWN

    def get_node_coordinates(self, node):
        game = self.games[self.current_game]
        x = game.x + (node[1] * HUNT_GAME_CONSTANTS.x_step)
        y = game.y + (node[0] * HUNT_GAME_CONSTANTS.y_step)
        return x, y

    def end_chapter(self):
        EndCurrentChapterAction(self.engine).perform()
