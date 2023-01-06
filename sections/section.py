import gzip
import os
import random
from math import sqrt

import numpy as np
import tcod
from pygame import mixer, sndarray

import tile_types
import xp_loader
from entities.entity import Entity
from entities.entity_loader import EntityLoader
from sections.section_layouts import full_fg_tile


class Section:
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = "", name: str =""):
        self.engine = engine

        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.entity_loader = EntityLoader(self.engine)
        self.entities = []

        tile = tile_types.background_tile
        tile["graphic"]["bg"] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.tiles =  np.full((self.width, self.height), fill_value=tile, order="F")
        self.ui = None

        xp_data = self.load_xp_data(xp_filepath)
        self.load_tiles(xp_filepath, xp_data)
        self.load_entities(xp_filepath, xp_data)

        self.invisible = False

    def load_xp_data(self, filepath):
        if filepath:
            try:
                xp_file = gzip.open("images/" + filepath)
                raw_data = xp_file.read()
                xp_file.close()
                return xp_loader.load_xp_string(raw_data)
            except:
                print(("Loading {0} failed!").format(filepath))

    def load_tiles(self, data_name, xp_data):
        if xp_data is not None:
            self.loaded_tiles = data_name
            for h in range(0, self.height):
                if h < xp_data['height']:
                    for w in range(0, self.width):
                        if w < xp_data['width']:
                            self.tiles[w, h]['walkable'] = True
                            self.tiles[w, h]['graphic'] = xp_data['layer_data'][0]['cells'][w][h]
                        else:
                            break
                else:
                    break

    def load_entities(self, data_name, xp_data):
        if xp_data is not None:
            if len(xp_data['layer_data']) > 1 != None:
                self.loaded_tiles = data_name
                for h in range(0, self.height):
                    if h < xp_data['height']:
                        for w in range(0, self.width):
                            if w < xp_data['width']:
                                self.entity_loader.load_entity(xp_data['layer_data'][1]['cells'][w][h][0], w, h, self)
                                pass
                            else:
                                break
                    else:
                        break

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            for entity in self.entities:
                if not entity.invisible:
                    console.print(entity.x, entity.y,entity.char, fg=entity.fg_color, bg=entity.bg_color)

    def render_ui(self, console):
        if not self.ui is None:
            self.ui.render(console)

    def update(self):
        for entity in self.entities:
            entity.update()

    def late_update(self):
        for entity in self.entities:
            entity.late_update()

    def refresh(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def mousedown(self,button,x,y):
        pass

    def mouseup(self,button,x,y):
        pass

    def keydown(self, key):
        for entity in self.entities:
            entity.keydown(key)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def get_entities_at_location(self, x: int, y: int):
        entities = list()
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                entities.append(entity)

        return entities

    def add_entity(self, entity):
        self.entities.append(entity)

    def is_point_in_section(self, x,y):
        return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)

    def get_moore_surrounding_tiles(self,x,y):
        tiles = list()
        tiles.append((x-1,y-1))
        tiles.append((x,y-1))
        tiles.append((x+1,y-1))
        tiles.append((x-1,y))
        tiles.append((x+1,y))
        tiles.append((x-1,y+1))
        tiles.append((x,y+1))
        tiles.append((x+1,y+1))

        return tiles

    def get_distance_between_tiles(self, a, b):
        return sqrt((abs(a[0]-b[0])**2) + (abs(a[1]-b[1])**2))

    def validate_sound(self, file):
        if os.path.isfile(file):
            sound = mixer.Sound(file)
            sound.set_volume(self.engine.save_data["volume"])
            return sound
        else:
            #Build fake sound for when the file can't be found, so everything hereafter works ok
            tmp = np.array([[0,0], [0,0]], np.int32)
            return sndarray.make_sound(tmp)

    def draw_button(self, console, bs):
        console.draw_frame(bs.x,bs.y,bs.width,bs.height, decoration=bs.decoration, bg=bs.bg, fg=bs.fg)
        mid_y = int(bs.height / 2)
        console.print_box(bs.x+1,bs.y +mid_y,bs.width-2,bs.height-2,string=bs.text,alignment=tcod.CENTER, bg=bs.font_bg, fg=bs.font_fg)

    def draw_image(self, console, rect, image):
        console.tiles_rgb[rect.x: rect.x + rect.width,rect.y: rect.y + rect.height] = image.tiles[0: rect.width, 0: rect.height]["graphic"]

    def draw_box(self, console, rect, decoration, margin, fg, bg):
        render_x = rect.x + margin
        render_y = rect.y + margin
        render_width =  rect.width - (margin * 2)
        render_height = rect.height - (margin * 2)

        console.draw_frame(x=render_x, y=render_y,width=render_width,height=render_height, decoration=decoration, bg=bg, fg=fg)

