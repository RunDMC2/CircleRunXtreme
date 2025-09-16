import random

from cfg import *


class Player:
    def __init__(self):
        self.color = BLUE
        self.radius = 15
        self.speed = 5
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.current_upgrade = None
        self.freeze_debuff = None
        self.froze_time = False
        self.love_mode = False
        self.xtreme_mode = False
        self.image = shading_img

    def move_left(self):
        self.x -= self.speed

        # wall collision
        if self.x - self.radius <= 0:
            self.x = 0 + self.radius

    def move_right(self):
        self.x += self.speed

        # wall collision
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius

    def move_up(self):
        self.y -= self.speed

        # wall collision
        if self.y - self.radius <= 0:
            self.y = 0 + self.radius

    def move_down(self):
        self.y += self.speed

        # wall collision
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        window.blit(pygame.transform.smoothscale(self.image, (self.radius*2, self.radius*2)), (self.x-self.radius, self.y-self.radius))


class Circle:
    def __init__(self, x, y):
        self.radius = circleRadius
        self.x = x
        self.y = y
        self.color = None
        self.image = None
        self.scoreValue = 0
        self.timeValue = 0

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        window.blit(pygame.transform.smoothscale(self.image, (circleRadius*2, circleRadius*2)), (self.x-circleRadius, self.y-circleRadius))

    def collide(self, player):
        del self


class RedCircle(Circle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = RED
        self.scoreValue = 1
        self.timeValue = FPS * 1
        self.image = red_circle_img

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds)-1)])
        circlesList.append(RedCircle(random.randint(circleRadius, WIDTH - circleRadius),
                                     random.randint(circleRadius, HEIGHT - circleRadius)))


class PurpleCircle(Circle):
    time_until_spawn_range = (5, 10)
    score_for_spawn = 0
    time_until_spawn = random.randint(FPS*time_until_spawn_range[0], FPS*time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = PURPLE
        self.scoreValue = 3
        self.timeValue = FPS * 3
        self.image = purple_circle_img

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds)-1)])


class YellowCircle(Circle):  # gives a random upgrade
    time_until_spawn_range = (15, 25)
    score_for_spawn = 5
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = YELLOW
        self.scoreValue = 1
        self.timeValue = FPS * 1
        self.image = yellow_circle_img

    def collide(self, player):
        pygame.mixer.Sound.play(powerup)

        # generates upgrade
        upgrade = upgrades[random.randint(0, len(upgrades) - 1)]
        player.current_upgrade = upgrade


class GreenCircle(Circle):  # makes circles tiny
    pass


class BlueCircle(Circle):  # freezes time (50% chance) or slows the player (25%) or freezes them completely (25%)
    time_until_spawn_range = (20, 55)
    score_for_spawn = 50
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = LIGHT_BLUE
        self.scoreValue = 0
        self.timeValue = 2 * FPS
        self.image = blue_circle_img

    def collide(self, player):
        # makes 50% chance of freezing time
        options = ["freeze time", "freeze time", "slow player", "freeze player"]
        player.freeze_debuff = options[random.randint(0, len(options) - 1)]

        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds) - 1)])

        if player.freeze_debuff == "freeze time":
            player.froze_time = True
        elif player.freeze_debuff == "slow player":
            player.speed = 3
        elif player.freeze_debuff == "freeze player":
            player.speed = 1


class OrangeCircle(Circle):  # takes away 1 second of time
    time_until_spawn_range = (20, 30)
    score_for_spawn = 30
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])
    OGTimeValue = FPS * (-1)
    timeValue = FPS * (-1)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = ORANGE
        self.scoreValue = 0
        self.timeValue = OrangeCircle.timeValue
        self.image = orange_circle_img

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds) - 1)])


class LimeCircle(Circle):  # takes away 3 seconds of time
    time_until_spawn_range = (50, 70)
    score_for_spawn = 40
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])
    OGTimeValue = FPS * (-3)
    timeValue = FPS * (-3)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = LIME
        self.scoreValue = 0
        self.timeValue = LimeCircle.timeValue
        self.image = lime_circle_img

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds) - 1)])


class PinkCircle(Circle):  # attracts ALL circles even bad
    time_until_spawn_range = (20, 45)
    score_for_spawn = 15
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = PINK
        self.scoreValue = 1
        self.timeValue = FPS * 1
        self.image = pink_circle_img

    def collide(self, player):
        player.love_mode = True


class WhiteCircle(Circle):  # makes you semi invisible
    pass


class BrownCircle(Circle):  # inverts your controls
    pass


class MaroonCircle(Circle):  # chases you until touch antidote circle
    pass


class BabyBlueCircle(Circle):  # only spawns if maroon is chasing and will kill maroon if collected
    pass


class RainbowCircle(Circle):
    time_until_spawn_range = (60, 200)  # 60 to 200
    score_for_spawn = 0
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = RED
        self.scoreValue = 1
        self.timeValue = 5 * FPS
        self.image = shading_img
        self.LorR = random.choice(["L", "R"])
        self.UorD = random.choice(["U", "D"])

    def collide(self, player):
        # get cool sound effect
        player.xtreme_mode = True


class LittleCircle(Circle):  # spawns only in extreme mode
    time_until_spawn = None
    score_for_spawn = None

    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = int(circleRadius // 2)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image = shading_img
        self.timeValue = 0

    def collide(self, player):
        # get petite sound effect
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds) - 1)])

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        window.blit(pygame.transform.smoothscale(self.image, (self.radius * 2, self.radius * 2)), (self.x - self.radius, self.y - self.radius))


circle_types = [
    PurpleCircle,
    YellowCircle,
    PinkCircle,
    BlueCircle,
    OrangeCircle,
    LimeCircle,
    RainbowCircle,
    LittleCircle
]

# circles for if more than one circle is allowed to spawn at once
repeat_spawn_circle_types = [
    OrangeCircle,
    LimeCircle
]

circle_descriptions = [
    "This circle will give 1 second and 1 point when popped. Keep popping them to stay in the game!",
    "Gives 3 points and 3 seconds, but appears less often than Red Circles!",
    "Gives a random upgrade between Extra points, Extra time, a Player size increase, or a Player speed increase!",
    "Makes ALL the circles attracted to you. Beware though, it will make bad circles come for you faster!",
    "Pop at your own risk! This circle will either freeze the timer, or freeze yourself!",
    "This circle will remove 1 second from the timer if you pop it, and 0.5 more for each subsequent one that's popped!",
    "This circle will remove 3 seconds from the timer if you pop it, and 1.5 more for each subsequent one that's popped!",
    "This elusive circle will activate Xtreme mode when popped! Pop it quickly before it disappears!",
    "These little circles will only appear after popping a Rainbow circle. They will give 0.5 seconds each when popped!"
]


circle_types_touched = [(RedCircle, True)]
for circle_type in circle_types:
    circle_types_touched.append((circle_type, False))

try:
    with open(get_asset_path("assets/save.pkl"), "rb") as f:
        circle_types_touched = pickle.load(f)[3]
except:
    pass


