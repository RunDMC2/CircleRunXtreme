import pygame
import math
import random
import pickle
from sys import exit
import os


pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Run Xtreme")
clock = pygame.time.Clock()

# stats for appearing circles
circlesList = []
circleRadius = 20

# images
title_background_image = pygame.image.load("../assets/gfcs/main_menu_bkg.png")
background_image = pygame.image.load("../assets/gfcs/bkg.jpg")

# <a href="https://www.freepik.com/free-vector/abstract-blue-circle-black-background-technology_32947947.htm#page=8
# &query=circle%20background&position=27&from_view=keyword&track=ais_user&uuid=bf43ac23-b562-4069-96b6-a9e13e2083a9
# ">Image by flatart</a> on Freepik
game_background_image = pygame.image.load("../assets/gfcs/game_bkg.jpg")

trophy = pygame.image.load("../assets/gfcs/trophy.png")
trophy_grey = pygame.image.load("../assets/gfcs/trophy_grey.png")

x_image = pygame.image.load("../assets/gfcs/x.png")

# sfx
pop1 = pygame.mixer.Sound("../assets/sfx/pop3.flac")
pop2 = pygame.mixer.Sound("../assets/sfx/pop4.flac")
pop3 = pygame.mixer.Sound("../assets/sfx/pop5.flac")
pop4 = pygame.mixer.Sound("../assets/sfx/pop7.flac")

pop_sounds = [pop1, pop2, pop3, pop4]

powerup = pygame.mixer.Sound("../assets/sfx/powerup.wav")

# upgrades
upgrades = [
    "Faster Movement Speed",
    "Player Size Increase",
    "Extra Points",
    "Extra Time",
]

# achievements
number_of_achievements = 18

achievements_list = {
    1: "Get a high score of 10 or more",
    2: "Get a high score of 30 or more",
    3: "Get a high score of 50 or more",
    4: "Get a high score of 100 or more",
    5: "Get a high score of 250 or more",
    6: "Get a high score of 500 or more",
    7: "Get a high score of 750 or more",
    8: "Get a high score of 999 or more",
    9: "Have 10 seconds of time at once",
    10: "Have 20 seconds of time at once",
    11: "Have 30 seconds of time at once",
    12: "Have 60 seconds of time at once",
    13: "Have 99 seconds of time at once",
    14: "Pop a total of 1000 circles: _/1000",
    15: "",
    16: "",
    17: "",
    18: ""
}

achievements_completion = []
for _ in range(number_of_achievements):
    achievements_completion.append(False)

time = FPS * 5
score = 0

arial40 = pygame.font.SysFont("Arial", 40)
bubble_font40 = pygame.font.Font("../assets/SuperFuntime-3zpLX.ttf", 40)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
BABY_BLUE = (175, 175, 255)
GREEN = (0, 255, 0)
LIME = (170, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
PINK2 = (255, 150, 180)
ORANGE = (255, 172, 28)


def rainbow(curr_color: tuple):
    r = curr_color[0]
    g = curr_color[1]
    b = curr_color[2]

    if curr_color[0] == 255 and curr_color[1] != 255 and curr_color[2] == 0:  # red -> orange -> yellow
        g += 5

    elif curr_color[0] != 0 and curr_color[1] == 255 and curr_color[2] != 255:  # yellow -> green
        r -= 5

    elif curr_color[0] == 0 and curr_color[1] == 255 and curr_color[2] != 255:  # green -> teal
        b += 15

    elif curr_color[0] == 0 and curr_color[1] != 0 and curr_color[2] == 255:  # teal -> blue
        g -= 5

    elif curr_color[0] != 255 and curr_color[1] == 0 and curr_color[2] == 255:  # blue -> purple
        r += 5

    elif curr_color[0] == 255 and curr_color[1] == 0 and curr_color[2] != 0:  # purple -> red
        b -= 5

    new_color = (r, g, b)

    return new_color


# file loading
try:
    with open("../assets/save.pkl", "rb") as f:
        achievements_completion = pickle.load(f)[0]
except:
    pass
