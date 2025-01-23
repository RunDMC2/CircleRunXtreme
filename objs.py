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


class Circle:
    def __init__(self, x, y):
        self.radius = circleRadius
        self.x = x
        self.y = y
        self.color = None
        self.scoreValue = 0
        self.timeValue = 0

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def collide(self, player):
        del self


class RedCircle(Circle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = RED
        self.scoreValue = 1
        self.timeValue = FPS * 1

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds)-1)])
        circlesList.append(RedCircle(random.randint(circleRadius, WIDTH - circleRadius),
                                     random.randint(circleRadius, HEIGHT - circleRadius)))


class PurpleCircle(Circle):
    time_until_spawn_range = (10, 20)
    score_for_spawn = 0
    time_until_spawn = random.randint(FPS*time_until_spawn_range[0], FPS*time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = PURPLE
        self.scoreValue = 3
        self.timeValue = FPS * 3

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds)-1)])


class YellowCircle(Circle):  # gives a random upgrade
    time_until_spawn_range = (15, 25)
    score_for_spawn = 10
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = YELLOW
        self.scoreValue = 1
        self.timeValue = FPS * 1

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
        self.timeValue = 0

    def collide(self, player):
        # makes 50% chance of freezing time
        options = ["freeze time", "freeze time", "slow player", "freeze player"]
        player.freeze_debuff = options[random.randint(0, len(options) - 1)]

        if player.freeze_debuff == "freeze time":
            player.froze_time = True
        elif player.freeze_debuff == "slow player":
            player.speed = 3
        elif player.freeze_debuff == "freeze player":
            player.speed = 0


class OrangeCircle(Circle):  # takes away 1 second of time
    time_until_spawn_range = (20, 30)
    score_for_spawn = 30
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = ORANGE
        self.scoreValue = 0
        self.timeValue = FPS * (-1)

    def collide(self, player):
        pygame.mixer.Sound.play(pop_sounds[random.randint(0, len(pop_sounds) - 1)])


class LimeCircle(Circle):  # takes away 3 seconds of time
    time_until_spawn_range = (50, 70)
    score_for_spawn = 40
    time_until_spawn = random.randint(FPS * time_until_spawn_range[0], FPS * time_until_spawn_range[1])

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = LIME
        self.scoreValue = 0
        self.timeValue = FPS * (-3)

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


circle_types = [
    PurpleCircle,
    YellowCircle,
    PinkCircle,
    BlueCircle,
    OrangeCircle,
    LimeCircle
]

# circles for if more than one circle is allowed to spawn at once
repeat_spawn_circle_types = [
    OrangeCircle,
    LimeCircle
]
