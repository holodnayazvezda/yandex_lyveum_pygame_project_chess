import pygame as pg

RES = WEDTH, HEIGHT = 600, 600

sc = pg.display.set_mode(RES)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLEDZOLOT = (238, 232, 170)
OHRA = (160, 82, 45)

FPS = 60

size = 75

clock = pg.time.Clock()

board = pg.Surface((600, 600))

for x in range(8):
    for y in range(8):
        if (x + y) % 2 == 0:
            pg.draw.rect(board, BLEDZOLOT, [size * x, size * y, size, size])
        else:
            pg.draw.rect(board, OHRA, [size * x, size * y, size, size])

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    sc.blit(board, (0, 0))

    pg.display.flip()
    clock.tick(FPS)