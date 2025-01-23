from objs import *
from button import *


def main_menu():
    while True:
        window.fill(BLACK)
        window.blit(title_background_image, (0, 0))

        # creates buttons
        play_button = Button((WIDTH/2 - 75, HEIGHT/2 - 45), (150, 75), WHITE, GREY, "Play", bubble_font40, None)
        quit_button = Button((WIDTH / 2 - 75, HEIGHT*31 / 40), (150, 75), WHITE, GREY, "Quit", bubble_font40, None)
        achievements_button = Button((WIDTH / 2 - 125, HEIGHT*3 / 5), (250, 75), WHITE, GREY, "Achievements", bubble_font40, None)
        options_button = Button((WIDTH - 170, HEIGHT - 95), (150, 75), WHITE, GREY, "Options", bubble_font40, None)

        mouse_pos = pygame.mouse.get_pos()

        if Game.high_score != 0:
            text = "High score: " + str(Game.high_score)
            text_rect = bubble_font40.render(text, True, BLACK)
            window.blit(text_rect, (10, HEIGHT - 50))

        # draws buttons
        for button in [play_button, quit_button, achievements_button, options_button]:
            button.change_color(mouse_pos)
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # if clicked on a button
                if play_button.is_hovered_over(mouse_pos):
                    play()
                elif quit_button.is_hovered_over(mouse_pos):
                    save()
                    pygame.quit()
                    exit()
                elif achievements_button.is_hovered_over(mouse_pos):
                    achievements_screen()
                elif options_button.is_hovered_over(mouse_pos):
                    options_screen()

        pygame.display.update()


def achievements_screen():
    # load achievement file data

    button_list = []
    back_button = Button((10, 10), (150, 75), WHITE, GREY, "Back", bubble_font40, None)
    button_list.append(back_button)

    # makes achievement buttons
    for i in range(3):
        for j in range(6):
            img = trophy_grey
            if achievements_completion[i*6+j]:
                img = trophy

            button_list.append(Button((17 + 80*j + 17*j, 120 + 80*i + 17*i), (80, 80), WHITE, GREY, " ", bubble_font40, img))

    while True:
        window.fill(BLACK)
        window.blit(background_image, (0, 0))

        text = bubble_font40.render("Achievements", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (300, 50)
        window.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        # draws buttons
        for button in button_list:
            button.change_color(mouse_pos)
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # if clicked on a button
                if back_button.is_hovered_over(mouse_pos):
                    main_menu()
                else:  # checks what achievement button was clicked
                    for button in button_list:
                        if button.is_hovered_over(mouse_pos):
                            achievement_popup(button_list.index(button), button.img)

        pygame.display.update()


def achievement_popup(achievement_num, img):
    x_button = Button((435, 85), (30, 30), WHITE, GREY, " ", bubble_font40, x_image)

    while True:
        # draws the pop up menu
        pygame.draw.circle(window, BLACK, (146, 96), 30)
        pygame.draw.circle(window, BLACK, (454, 96), 30)
        pygame.draw.circle(window, BLACK, (146, 504), 30)
        pygame.draw.circle(window, BLACK, (454, 504), 30)

        pygame.draw.rect(window, BLACK, (116, 96, 60, 408))
        pygame.draw.rect(window, BLACK, (424, 96, 60, 408))
        pygame.draw.rect(window, BLACK, (146, 66, 308, 60))
        pygame.draw.rect(window, BLACK, (146, 474, 308, 60))

        pygame.draw.circle(window, WHITE, (150, 100), 30)
        pygame.draw.circle(window, WHITE, (450, 100), 30)
        pygame.draw.circle(window, WHITE, (150, 500), 30)
        pygame.draw.circle(window, WHITE, (450, 500), 30)

        pygame.draw.rect(window, WHITE, (120, 100, 60, 400))
        pygame.draw.rect(window, WHITE, (420, 100, 60, 400))
        pygame.draw.rect(window, WHITE, (150, 70, 300, 60))
        pygame.draw.rect(window, WHITE, (150, 470, 300, 60))

        pygame.draw.rect(window, WHITE, (180, 130, 240, 340))

        mouse_pos = pygame.mouse.get_pos()

        for button in [x_button]:
            button.change_color(mouse_pos)
            button.draw(window)

        # text
        text = "Achievement " + str(achievement_num)
        text = bubble_font40.render(text, True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (300, 150)
        window.blit(text, text_rect)

        # achievement desc
        text = achievements_list[achievement_num]
        if achievement_num == 14:  # achievement #14 requirement
            text = f"Pop a total of 1000 circles: {Game.total_circles_popped}/1000"
        wrap_text(180, 420, 350, text)

        # trophy
        window.blit(img, (260, 190))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.is_hovered_over(mouse_pos):
                    achievements_screen()

        pygame.display.update()


def wrap_text(x_start, x_end, y_start, text: str):
    x_curr = x_start
    x_center = ((x_end - x_start) / 2) + x_start
    y_curr = y_start
    words = text.split(" ")
    curr_str = ""

    for word in words:
        rendered_word = bubble_font40.render(word, True, BLACK)
        if x_curr + rendered_word.get_width() + 33 >= x_end:
            # blit the line that has no more room
            rendered_line = bubble_font40.render(curr_str, True, BLACK)
            word_rect = rendered_line.get_rect()
            word_rect.center = (x_center, y_curr)
            window.blit(rendered_line, word_rect)

            # start new line
            y_curr += 40
            x_curr = x_start
            curr_str = word + " "
        else:
            # adds word to current line
            curr_str = curr_str + word + " "
            x_curr += rendered_word.get_width() + 11

    # renders the last few words that don't form a whole line
    rendered_line = bubble_font40.render(curr_str, True, BLACK)
    word_rect = rendered_line.get_rect()
    word_rect.center = (x_center, y_curr)
    window.blit(rendered_line, word_rect)


def options_screen():
    back_button = Button((10, 10), (150, 75), WHITE, GREY, "Back", bubble_font40, None)

    save_button = Button((WIDTH / 2 - 75, 100), (150, 75), WHITE, GREY, "Save", bubble_font40, None)
    load_button = Button((WIDTH / 2 - 75, 205), (150, 75), WHITE, GREY, "Load", bubble_font40, None)
    wipe_button = Button((WIDTH / 2 - 95, 310), (190, 75), WHITE, GREY, "Wipe Data", bubble_font40, None)

    saving = False
    loading = False
    wiping = False

    while True:
        window.fill(BLACK)
        window.blit(background_image, (0, 0))

        text = bubble_font40.render("Options", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (300, 50)
        window.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        for button in [back_button, save_button, load_button, wipe_button]:
            button.change_color(mouse_pos)
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # if clicked on a button
                if back_button.is_hovered_over(mouse_pos):
                    saving = False
                    loading = False
                    wiping = False
                    main_menu()

                elif save_button.is_hovered_over(mouse_pos):
                    loading = False
                    wiping = False
                    saving = True
                    save()

                elif load_button.is_hovered_over(mouse_pos):
                    saving = False
                    loading = True
                    wiping = False
                    load()

                elif wipe_button.is_hovered_over(mouse_pos):
                    saving = False
                    loading = False
                    wiping = True
                    wipe()

        if saving:
            text = bubble_font40.render("Data has been saved", True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH / 2, 500)
            window.blit(text, text_rect)
        elif loading:
            text = bubble_font40.render("Data has been restored", True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH / 2, 500)
            window.blit(text, text_rect)
        elif wiping:
            text = bubble_font40.render("Data has been deleted", True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH / 2, 500)
            window.blit(text, text_rect)

        pygame.display.update()


def play():
    player = Player()

    game = Game(player)

    # creates the first circle object
    circlesList.clear()
    circlesList.append(RedCircle(random.randint(circleRadius, WIDTH - circleRadius),
                                 random.randint(circleRadius, HEIGHT - circleRadius)))

    # starts the main loop of the game
    while True:
        game.main()


def save():
    # dumps all savable variables as a tuple to be accessed from .pkl file
    with open("../assets/save.pkl", "wb") as f:
        pickle.dump((achievements_completion, Game.high_score, Game.total_circles_popped), f)


def load():
    try:
        with open("../assets/save.pkl", "rb") as f:
            Game.high_score = pickle.load(f)[1]
    except:
        pass
    try:
        with open("../assets/save.pkl", "rb") as f:
            Game.total_circles_popped = pickle.load(f)[2]
    except:
        pass

    for ind, ach in enumerate(achievements_completion):
        try:
            with open("../assets/save.pkl", "rb") as f:
                achievements_completion[ind] = pickle.load(f)[0][ind]
        except:
            pass


def wipe():
    # Resets all saved vars to normal then deletes save file
    Game.high_score = 0
    Game.total_circles_popped = 0
    for ind, ach in enumerate(achievements_completion):
        achievements_completion[ind] = False

    try:
        os.remove("../assets/save.pkl")
    except:
        pass


class Game:
    total_circles_popped = 0
    high_score = 0
    try:
        with open("../assets/save.pkl", "rb") as f:
            high_score = pickle.load(f)[1]
    except:
        pass
    try:
        with open("../assets/save.pkl", "rb") as f:
            total_circles_popped = pickle.load(f)[2]
    except:
        pass

    def __init__(self, player):
        self.time = time
        self.score = score
        self.player = player

        self.upgrade_timer = FPS * 10
        self.love_mode_timer = FPS * 10
        self.freeze_timer = FPS * 7

    def main(self):  # main loop
        self.events()
        self.actions()
        self.timers()
        self.draw()
        self.achievements_check()
        clock.tick(FPS)

    def events(self):  # deals with user events e.g. keystrokes
        for event in pygame.event.get():
            # close window
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        i = 0
        j = 0

        if keys[pygame.K_LEFT]:
            i -= 1
        if keys[pygame.K_RIGHT]:
            i += 1
        if keys[pygame.K_UP]:
            j -= 1
        if keys[pygame.K_DOWN]:
            j += 1

        # corrects diagonal movement
        if i != 0 and j != 0:
            self.player.speed *= math.sqrt(2)/2

        if keys[pygame.K_LEFT]:
            self.player.move_left()

        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        if keys[pygame.K_UP]:
            self.player.move_up()

        if keys[pygame.K_DOWN]:
            self.player.move_down()

        # corrects speed so diagonal speed is maintained
        if i != 0 and j != 0:
            self.player.speed /= math.sqrt(2)/2
            self.player.speed = int(self.player.speed)

    def actions(self):  # deals with in-game actions e.g. collision
        # all collision
        for circle in circlesList:
            dist = math.sqrt(((circle.y - self.player.y) ** 2) + ((circle.x - self.player.x) ** 2))

            # love mode circle attraction
            if self.player.love_mode:
                circle.x += (self.player.x - circle.x) * (150 / (dist ** 2))
                circle.y += (self.player.y - circle.y) * (150 / (dist ** 2))

            # makes bad circles come towards you too
            if any(isinstance(circle, c) for c in repeat_spawn_circle_types):
                circle.x += (self.player.x - circle.x) * (150 / (dist ** 2))
                circle.y += (self.player.y - circle.y) * (150 / (dist ** 2))

            if dist < circle.radius + self.player.radius:
                circle.collide(self.player)

                self.time += circle.timeValue
                # adds extra time if has upgrade
                if self.player.current_upgrade == "Extra Time":
                    # adds extra half second of time if good circle, removes double time if bad
                    if circle.timeValue > 0:
                        self.time += int(FPS * 0.5)
                    elif circle.timeValue < 0:
                        self.time += circle.timeValue

                self.score += circle.scoreValue
                # adds extra points if has upgrade
                if self.player.current_upgrade == "Extra Points":
                    if circle.scoreValue != 0:
                        self.score += 2

                circlesList.remove(circle)

                # achievement #14
                if Game.total_circles_popped < 1000:
                    Game.total_circles_popped += 1
                if Game.total_circles_popped == 1000:
                    achievements_completion[13] = True

        # upgrade effects
        self.player.radius = 15
        if self.player.current_upgrade is None and self.player.freeze_debuff is None:
            self.player.speed = 5
        if self.player.current_upgrade == "Faster Movement Speed":
            if self.player.freeze_debuff != "freeze player":
                self.player.speed = 8
        elif self.player.current_upgrade == "Player Size Increase":
            self.player.radius = 35

        # check if conflicting upgrade and debuff are activated
        if self.player.current_upgrade == "Faster Movement Speed" and self.player.freeze_debuff == "slow player":
            self.player.speed = 5

        # check if circles are ready to be spawned
        for circle_type in circle_types:
            if circle_type.time_until_spawn == 0:
                valid_circle_pos = False

                # makes new circle spawn far enough away from the player
                while not valid_circle_pos:
                    x = random.randint(circleRadius, WIDTH - circleRadius)
                    y = random.randint(circleRadius, HEIGHT - circleRadius)

                    if abs(x - self.player.x) > 60 and abs(y - self.player.y) > 60:
                        valid_circle_pos = True

                new_circle = circle_type(x, y)
                circlesList.append(new_circle)
                circle_type.time_until_spawn = random.randint(FPS * circle_type.time_until_spawn_range[0],
                                                              FPS * circle_type.time_until_spawn_range[1])

        # upgrade time reset
        if self.upgrade_timer == 0:
            self.player.current_upgrade = None
            self.player.color = BLUE
            self.upgrade_timer = FPS * 10

        # love mode reset
        if self.love_mode_timer == 0:
            self.player.love_mode = False
            self.love_mode_timer = FPS * 10

        # freezing timer reset
        if self.freeze_timer == 0:
            self.player.freeze_debuff = None
            self.player.speed = 5
            self.player.froze_time = False
            self.freeze_timer = FPS * 7

    def timers(self):  # deals with timers and rng of objects
        if self.player.freeze_debuff == "freeze time":
            pass
        else:
            self.time -= 1
        # lose condition
        if self.time <= 0:

            if self.score > Game.high_score:
                Game.high_score = self.score
                self.achievements_check()

            main_menu()

        # prepares for next circle spawning if conditions are met (not already one spawned and score requirement)
        for circle_type in circle_types:
            if self.score >= circle_type.score_for_spawn and (not any(isinstance(c, circle_type) for c in circlesList)):
                circle_type.time_until_spawn -= 1

        # for repeat spawning circles they will continuously spawn
        for circle_type in repeat_spawn_circle_types:
            if self.score >= circle_type.score_for_spawn and (any(isinstance(c, circle_type) for c in circlesList)):
                circle_type.time_until_spawn -= 1

        # upgrades
        if self.player.current_upgrade is not None:
            self.upgrade_timer -= 1

        # freeze debuff timer
        if self.player.freeze_debuff is not None:
            self.freeze_timer -= 1

        # love mode (pink)
        if self.player.love_mode:
            self.love_mode_timer -= 1

    def achievements_check(self):  # checks if you've completed an achievement
        # achievement #1
        if Game.high_score >= 10:
            achievements_completion[0] = True
        # achievement #2
        if Game.high_score >= 30:
            achievements_completion[1] = True
        # achievement #3
        if Game.high_score >= 50:
            achievements_completion[2] = True
        # achievement #4
        if Game.high_score >= 100:
            achievements_completion[3] = True
        # achievement #5
        if Game.high_score >= 250:
            achievements_completion[4] = True
        # achievement #6
        if Game.high_score >= 500:
            achievements_completion[5] = True
        # achievement #7
        if Game.high_score >= 750:
            achievements_completion[6] = True
        # achievement #8
        if Game.high_score >= 999:
            achievements_completion[7] = True

        # achievement #9
        if self.time >= FPS * 10:
            achievements_completion[8] = True
        # achievement #10
        if self.time >= FPS * 20:
            achievements_completion[9] = True
        # achievement #11
        if self.time >= FPS * 30:
            achievements_completion[10] = True
        # achievement #12
        if self.time >= FPS * 60:
            achievements_completion[11] = True
        # achievement #13
        if self.time >= FPS * 99:
            achievements_completion[12] = True

    def draw(self):  # draws stuff to the screen
        window.fill(BLACK)
        window.blit(game_background_image, (-240, 0))

        if self.player.current_upgrade is not None:
            self.player.color = rainbow(self.player.color)

        self.player.draw()

        for circle in circlesList:
            circle.draw()

        # text
        # time
        text = str(self.time // 60) + "." + str((self.time / 60 - self.time // 60 + 1) * 100)[1:3]
        text_rect = bubble_font40.render(text, True, WHITE)
        text_rect_rect = text_rect.get_rect()
        text_rect_rect.center = (WIDTH/2, 25)
        window.blit(text_rect, text_rect_rect)
        # score
        text = str(self.score)
        text_rect = bubble_font40.render(text, True, WHITE)
        window.blit(text_rect, (5, 5))
        # upgrade
        if self.player.current_upgrade is not None:
            text = str(self.player.current_upgrade)
            text_rect = bubble_font40.render(text, True, WHITE)
            window.blit(text_rect, (5, HEIGHT - 45))
        # freeze debuff
        if self.player.freeze_debuff is not None:
            text = str(self.player.freeze_debuff)
            text_rect = bubble_font40.render(text, True, WHITE)
            window.blit(text_rect, (WIDTH - 100, HEIGHT - 45))
        # love mode
        if self.player.love_mode:
            # draws a heart
            pygame.draw.circle(window, PINK2, (WIDTH - 40, 20), 10)
            pygame.draw.circle(window, PINK2, (WIDTH - 25, 20), 10)
            pygame.draw.polygon(window, PINK2, [(WIDTH - 47, 26), (WIDTH - 19, 26), (WIDTH - 33, 40)])

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
