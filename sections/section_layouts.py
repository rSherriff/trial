from typing import NamedTuple

INTRO_SECTION = "introSection"
MENU_SECTION = "menuSection"
HUNT_SECTION = "huntSection"
TITLE_SECTION = "titleSection"

SCREEN_WIDTH = 51
SCREEN_HEIGHT = 30

dialog_box_decoration =  chr(198) + chr(9608) + chr(201) + chr(9608)+ " "+ chr(9608) + chr(244)+ chr(9608)+ chr(230)
dialog_box_decoration_filled =  chr(198) + chr(9608) + chr(201) + chr(9608)+ chr(9608)+ chr(9608) + chr(244)+ chr(9608)+ chr(230)

button_box_decoration  =  chr(238) + chr(9604) + chr(232) + chr(9616)+ chr(9608)+chr(9612)+ chr(239) + chr(9600)+ chr(235)

black = (0,0,0)
white = (255,255,255)
grey=(158,158,158)
pink = (255,51,102)
orange = (255,191,0)
red=(255,0,0)

main_background = (23,18,25)

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
    "text_color":(255,255,255)
}