from cfg import *


class Button:
    def __init__(self, pos: tuple, size: tuple, color_def, color_hov, text, font, img):
        self.x, self.y = pos
        self.width, self.height = size
        self.color_def = color_def
        self.color_hov = color_hov
        self.font = font
        self.text = self.font.render(text, True, BLACK)
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.rect_color = self.color_def
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        self.img = None
        if img is not None:
            self.img = img

    def draw(self, screen):
        pygame.draw.rect(screen, self.rect_color, self.rect)
        screen.blit(self.text, self.text_rect)
        if self.img is not None:
            screen.blit(self.img, (self.x, self.y))

    def is_hovered_over(self, mouse_pos: tuple):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False

    def change_color(self, mouse_pos: tuple):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.rect_color = self.color_hov
        else:
            self.rect_color = self.color_def

