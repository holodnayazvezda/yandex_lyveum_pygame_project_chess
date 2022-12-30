import pygame


class Button():
    def __init__(self, screen, x, y, width, height, buttonText='Button',
                 onclickFunction=None, value=1, onePress=False, font_type='Arial', font_size=40):
        self.font = pygame.font.SysFont(font_type, font_size)
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if not value and value != 0:
            self.onclickFunction = lambda: onclickFunction()
        else:
            self.onclickFunction = lambda: onclickFunction(value)
        self.onePress = onePress

        self.fillColors = {
            'normal': (210, 210, 210),
            'hover': (100, 100, 100),
            'pressed': (50, 50, 50),
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
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
