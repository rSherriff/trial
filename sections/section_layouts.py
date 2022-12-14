from typing import NamedTuple
from image import Image

INTRO_SECTION = "introSection"
MENU_SECTION = "menuSection"
HUNT_SECTION = "huntSection"
TITLE_SECTION = "titleSection"
PURGE_SECTION = "purgeSection"

SCREEN_WIDTH = 51
SCREEN_HEIGHT = 30

dialog_box_decoration =  chr(198) + chr(9608) + chr(201) + chr(9608)+ " "+ chr(9608) + chr(244)+ chr(9608)+ chr(230)
dialog_box_decoration_filled =  chr(198) + chr(9608) + chr(201) + chr(9608)+ chr(9608)+ chr(9608) + chr(244)+ chr(9608)+ chr(230)

button_box_decoration  =  chr(238) + chr(9604) + chr(232) + chr(9616)+ chr(9608)+chr(9612)+ chr(239) + chr(9600)+ chr(235)

full_fg_tile = 9608

black = (0,0,0)
white = (255,255,255)
grey=(158,158,158)
pink = (255,51,102)
orange = (255,191,0)
red=(255,0,0)

main_background = (23,18,25)
land_green = (64,102,63)

main_text = (255,255,255)

class Rect(NamedTuple):
    x : int
    y : int
    width : int
    height : int

class Position(NamedTuple):
    x : int
    y : int

class Button(NamedTuple):
    text : str
    x : int
    y : int
    width : int
    height : int
    bg : tuple
    fg: tuple
    h_fg: tuple
    font_bg : tuple
    font_fg : tuple
    decoration: list

class ImageRect(NamedTuple):
    rect : Rect
    image:Image

menu_section_layout = {
    "start_button": Button(text="Start",x=22,y=25,width=7,height=3,bg=black,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "charles_frame_one":Rect(0,0,9,14),
    "charles_frame_two":Rect(10,0,9,14),
    "charles_rect":Rect(20,5,9,14),
}

confirmation_dialog_info = {
    "dialog_decoration":dialog_box_decoration_filled,
    "button_decoration":button_box_decoration,
    "fg_color":white,
    "bg_color":black,
    "b_fg_color": white,
    "b_bg_color":white,
    "b_h_color":pink,
    "b_font_fg_color":grey,
    "b_font_bg_color":white,
    "max_width" : 40,
    "button_width" : 3,
    "button_height": 3
}

notification_dialog_info = {
    "dialog_decoration":dialog_box_decoration_filled,
    "button_decoration":button_box_decoration,
    "fg_color":white,
    "bg_color":black,
    "b_fg_color": white,
    "b_bg_color":white,
    "b_h_color":pink,
    "b_font_fg_color":grey,
    "b_font_bg_color":white,
    "max_width" : 40,
    "button_width" : 7,
    "button_height": 3
}

title_section_info = {
    "title" : Rect(1, 3, SCREEN_WIDTH - 2, 1),
    "main_text":Rect(int(SCREEN_WIDTH*0.1), int(SCREEN_HEIGHT*0.25), int(SCREEN_WIDTH*0.8), int(SCREEN_HEIGHT*0.5)),
    "start_button": Button(text="Start",x=22,y=25,width=7,height=3,bg=black,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "start_wait_time": 2.0,
    "title_time": 4.0,
    "title_fade_time" : 2.0,
    "text_color":(255,255,255),
    "text_pause_time": 2.0,
}

hunt_section_info = {
    "quit_button": Button(text="Quit",x=7,y=25,width=6,height=3,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_open_button": Button(text="Instructions",x=3,y=22,width=14,height=3,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_close_button": Button(text="Close",x=23,y=19,width=7,height=3,bg=black,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_image": ImageRect(Rect(8,3,36,21), Image(0,0,36,21, "images/hunt_instructions.xp")),
    "advisor_dialog_rect": Rect(19,3,25, 20),
    "advisor_dialog_decoration":dialog_box_decoration_filled,
    "advisor_dialog_margin":-1,
    "advisor_dialog_bg": main_background,
    "advisor_dialog_fg": white,
    "advisor_dialog_text_color": grey,
    "start_wait_time": 2.0,
    "setup_wait_time": 1.0,
    "see_instructions_wait_time" : 0.7,
    "speech_mark_image": ImageRect(Rect(17,6,1,1),Image(0,0,1,1, "images/misc.xp")),
    "advisor_top_eyes_open": ImageRect(Rect(4,3,13,7), Image(0,0,13,7, "images/advisor.xp")),
    "advisor_top_eyes_closed": ImageRect(Rect(4,3,13,7), Image(13,0,13,7, "images/advisor.xp")),
    "advisor_btm_mouth_closed": ImageRect(Rect(4,10,13,8), Image(0,7,13,8, "images/advisor.xp")),
    "advisor_btm_mouth_open": ImageRect(Rect(4,10,13,8), Image(13,7,13,8, "images/advisor.xp")),
    "advisor_btm_mouth_open": ImageRect(Rect(4,10,13,8), Image(13,7,13,8, "images/advisor.xp")),
    "game_grid_3x3": ImageRect(Rect(33,14,7,7), Image(0,0,7,7, "images/hunt_grids.xp")),
    "game_grid_4x4": ImageRect(Rect(31,12,9,9), Image(7,0,9,9, "images/hunt_grids.xp")),
    "game_grid_5x5": ImageRect(Rect(29,10,11,11), Image(16,0,11,11, "images/hunt_grids.xp")),
    
}

purge_section_info = {
    "roll_button": Button(text="Roll",x=39,y=25,width=6,height=3,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_open_button": Button(text="Instructions",x=2,y=25,width=14,height=3,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_close_button": Button(text="Close",x=23,y=19,width=7,height=3,bg=black,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "instructions_image": ImageRect(Rect(8,3,36,21), Image(0,0,36,21, "images/purge_instructions.xp")),
    "pass_button": Button(text="Pass",x=26,y=24,width=8,height=5,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    "bar_button": Button(text="Bar",x=19,y=24,width=7,height=5,bg=main_background,fg=white,font_fg=grey,h_fg=pink,font_bg=white,decoration=button_box_decoration),
    
    "pride_dialog_rect": Rect(17,14,19,9),
    "pride_character": ImageRect(Rect(38,7,9,14), Image(0,0,9,14, "images/pride.xp")),
    "pride_eyes_open": ImageRect(Rect(42,10,3,1), Image(10,1,3,1, "images/pride.xp")),
    "pride_eyes_closed": ImageRect(Rect(42,10,3,3), Image(10,2,3,1, "images/pride.xp")),
    "pride_mouth_closed": ImageRect(Rect(43,13,1,1), Image(10,0,1,1, "images/pride.xp")),
    "pride_mouth_open": ImageRect(Rect(43,13,1,1), Image(11,0,1,1, "images/pride.xp")),
    "pride_speech_mark_image": ImageRect(Rect(37,15,1,1),Image(2,0,1,1, "images/misc.xp")),

    "member_dialog_rect": Rect(16,7,19,9),
    "member_animation_rects":{"eo":Rect(8,10,3,1), "ec": Rect(8,10,3,1), "mo":Rect(9,13,1,1), "mc":Rect(9,13,1,1,)},
    "member_speech_mark_image": ImageRect(Rect(14,9,1,1),Image(0,0,1,1, "images/misc.xp")),
    "member_1_character": ImageRect(Rect(4,7,9,14), Image(0,0,9,14, "images/pride.xp")),
    "member_1_frames":{"eo":Image(10,1,3,1, "images/pride.xp"), "ec": Image(10,2,3,1, "images/pride.xp"), "mo":Image(11,0,1,1, "images/pride.xp"), "mc":Image(10,0,1,1, "images/pride.xp")},

    "dialog_decoration":dialog_box_decoration_filled,
    "dialog_margin":-1,
    "dialog_bg": main_background,
    "dialog_fg": white,
    "text_color": grey,
    "start_wait_time": 2.0,

    "member_dialog_wait_time":2.0,
    "pride_dialog_wait_time":2.0,
    "transition_wait_time": 1.0,
}