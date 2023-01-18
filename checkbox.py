# файл в котором реализуется логика работы чекбокса

import pygame


class CheckBox:
    def __init__(self, surface, x, y, caption="", is_active=False, font_size=25, color=(230, 230, 230),
                 outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_color=(255, 255, 255), text_offset=(40, 1), font='Open Sans'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 30, 30)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = is_active

    def _draw_button_text(self):
        self.font = pygame.font.SysFont('Arial', self.fs, True)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 30 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 15, self.y + 15), 10)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        # здесь я ставлю 700 для того, чтобы чекбокс работал не только при нажатии на него, но и при нажатии на текст
        # так лучше не делать, если текст масштабируется, но посколько я точно знаю его длину, то могу себе позволить ;)
        if px < x < 700 and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN and event_object.button == 1:
            self._update()
