import pygame
from config import ENGLISH_ALPHABED, RUSSIAN_ALPHABED, NUMBERS
pygame.init()


class InputBox:

    def __init__(self, x, y, w, h,  color_inactve=pygame.Color('lightskyblue3'),
                 color_active=pygame.Color('dodgerblue2'), font=pygame.font.Font(None, 27)):
        # инициализируем переданные переменные
        self.COLOR_INACTIVE = color_inactve
        self.COLOR_ACTIVE = color_active
        self.FONT = font
        # создаем необходимые параметры
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactve
        self.text = ''
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in ENGLISH_ALPHABED + RUSSIAN_ALPHABED + NUMBERS + " ":
                        if len(self.text) <= 18:
                            self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
