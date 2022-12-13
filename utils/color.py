
import random


red =  (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

colors = []
colors.append(red)
colors.append(green)
colors.append(blue)
colors.append(yellow)

def get_random_color():
    return colors[random.randrange(0, len(colors))]

def blend_colour(lc, rc, t):
    r = lc[0] * t + rc[0] * (1 - t) 
    g = lc[1] * t + rc[1] * (1 - t) 
    b = lc[2] * t + rc[2] * (1 - t)

    return (int(r),int(g),int(b))