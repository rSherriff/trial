from sections.section_layouts import HUNT_SECTION

intro_splashes= (
    { "type": "IMAGE", "intro": 2, "hang": 3, "outro": 2, "file": "images/intro1.xp", "width": -1, "height": -1 },
    { "type": "IMAGE", "intro": 2, "hang": 3, "outro": 0, "file": "images/intro3.xp", "width": -1, "height": -1 },
    { "type": "SOUND", "file": "menu.mp3", "keep_into_menu": True }
)

chapters = {
  "hunt":{
    "title": "Part 1: The Hunt",
    "text":"Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    "instruction":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "stage":HUNT_SECTION,
  }
}
  

