import pygame
import math
import random
import pickle
from sys import exit
import os
import sys

def get_asset_path(relative_path):
    #if hasattr(sys, '_MEIPASS'):
         # UNCOMMENT TO MAKE BUNDLED EXE THAT CAN BE MOVED ANYWHERE (Saving won't work)
        #return os.path.join(sys._MEIPASS, relative_path)

    return relative_path


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
title_background_image = pygame.image.load(get_asset_path("assets/gfcs/new_main_menu_bkg.png"))
background_image = pygame.image.load(get_asset_path("assets/gfcs/new_bkg.png"))

shading_img = pygame.image.load(get_asset_path("assets/gfcs/shading.png"))
red_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Red.png"))
yellow_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Yellow.png"))
yellow_circle_img = pygame.image.load(get_asset_path("assets/gfcs/YellowUp.png"))
purple_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Purple.png"))
blue_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Light Blue.png"))
blue_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Light Blue Snow.png"))
orange_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Orange.png"))
pink_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Pink.png"))
lime_circle_img = pygame.image.load(get_asset_path("assets/gfcs/Lime.png"))
locked_circle = pygame.image.load(get_asset_path("assets/gfcs/Grey.png"))
rainbow_circle = pygame.image.load(get_asset_path("assets/gfcs/Rainbow.png"))

game_background_image = pygame.image.load(get_asset_path("assets/gfcs/new_game_bkg_v2.png"))

trophy = pygame.image.load(get_asset_path("assets/gfcs/trophy.png"))
trophy_grey = pygame.image.load(get_asset_path("assets/gfcs/trophy_grey.png"))

x_image = pygame.image.load(get_asset_path("assets/gfcs/x.png"))

# sfx
pop1 = pygame.mixer.Sound(get_asset_path("assets/sfx/pop3.flac"))
pop2 = pygame.mixer.Sound(get_asset_path("assets/sfx/pop4.flac"))
pop3 = pygame.mixer.Sound(get_asset_path("assets/sfx/pop5.flac"))
pop4 = pygame.mixer.Sound(get_asset_path("assets/sfx/pop7.flac"))

pop_sounds = [pop1, pop2, pop3, pop4]

powerup = pygame.mixer.Sound(get_asset_path("assets/sfx/powerup.wav"))
powerup.set_volume(0.3)

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
    15: "More coming soon!",
    16: "More coming soon!",
    17: "More coming soon!",
    18: "More coming soon!"
}

achievements_completion = []
for _ in range(number_of_achievements):
    achievements_completion.append(False)

time = FPS * 5
score = 0

arial40 = pygame.font.SysFont("Arial", 40)
bubble_font40 = pygame.font.Font(get_asset_path("assets/SuperFuntime-3zpLX.ttf"), 40)
bubble_font25 = pygame.font.Font(get_asset_path("assets/SuperFuntime-3zpLX.ttf"), 25)
bubble_font15 = pygame.font.Font(get_asset_path("assets/SuperFuntime-3zpLX.ttf"), 15)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
DARK_GREY = (150, 150, 150)
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


indicators = []
indicators_on_screen = []

text_speed = 1
alpha_speed = 1

def draw_indicators():
    if len(indicators) != len(indicators_on_screen):
        alpha = 100
        score_color = GREEN
        time_color = GREEN
        x = 30
        y = 70

        x_t = WIDTH / 2
        y_t = 70


        if indicators[-1][0] == 0 or indicators[-1][0] is None:
            scr = ""
        elif indicators[-1][0] < 0:
            scr = "-" + str(indicators[-1][0])
            score_color = RED
        else:
            scr = "+" + str(indicators[-1][0])


        if indicators[-1][1]/FPS == 0 or indicators[-1][1]/FPS is None:
            tim = ""
        elif indicators[-1][1]/FPS < 0:
            tim = str(round(indicators[-1][1] / FPS, 2))
            if len(str(indicators[-1][1] / FPS).split(".")) > 1 and len(str(indicators[-1][1] / FPS).split(".")[-1]) == 1:
                tim = str(round(indicators[-1][1] / FPS, 2)) + "0"
            time_color = RED
        else:
            tim = "+" + str(round(indicators[-1][1]/FPS, 2))
            if len(str(indicators[-1][1] / FPS).split(".")) > 1 and len(str(indicators[-1][1] / FPS).split(".")[-1]) == 1:
                tim = "+" + str(round(indicators[-1][1] / FPS, 2)) + "0"


        score_text = bubble_font25.render(scr, True, score_color)
        alpha_score_text = pygame.Surface(score_text.get_size()).convert_alpha()
        alpha_score_text.fill((score_color[0], score_color[1], score_color[2], alpha))
        score_text.blit(alpha_score_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        time_text = bubble_font25.render(tim, True, time_color)
        alpha_time_text = pygame.Surface(time_text.get_size()).convert_alpha()
        alpha_time_text.fill((time_color[0], time_color[1], time_color[2], alpha))
        time_text.blit(alpha_time_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        window.blit(score_text, (x, y))
        window.blit(time_text, (x_t, y_t))

        indicators_on_screen.append((score_text, alpha_score_text, alpha, y, x, time_text, x_t, y_t))

    else:
        for i in range(0, len(indicators_on_screen)):
            try:
                element = indicators_on_screen[i]
                new_alpha = element[2] - alpha_speed

                new_alpha_text = pygame.Surface(element[0].get_size()).convert_alpha()
                #new_alpha_text.fill((GREEN[0], GREEN[1], GREEN[2], new_alpha))

                new_tup = (element[0], new_alpha_text, new_alpha, element[3] - text_speed, element[4], element[5], element[6], element[7] - text_speed)
                indicators_on_screen[i] = new_tup

                window.blit(new_tup[0], (new_tup[4], new_tup[3]))
                window.blit(new_tup[5], (new_tup[6], new_tup[7]))

                if new_tup[2] == 0:
                    indicators_on_screen.remove(indicators_on_screen[i])
                    indicators.remove(indicators[i])
                    i -= 1
            except:
                continue



# file loading
try:
    with open(get_asset_path("assets/save.pkl"), "rb") as f:
        achievements_completion = pickle.load(f)[0]
except:
    pass
