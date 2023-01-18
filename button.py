# файл в котором реализуется логика кнопки

import pygame


class Button:
    def __init__(self, screen, x, y, width, height, button_text='Button',
                 on_click_function=None, value=1, one_press=False, font_type='Arial', font_size=40):
        self.font = pygame.font.SysFont(font_type, font_size)
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = button_text
        if not value and value != 0:
            self.onclickFunction = lambda: on_click_function()
        else:
            self.onclickFunction = lambda: on_click_function(value)
        self.onePress = one_press

        self.fillColors = {
            'normal': (210, 210, 210),
            'hover': (100, 100, 100),
            'pressed': (50, 50, 50),
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(self.buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):

        mouse_pos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)
