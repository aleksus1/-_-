import pygame as pg
from pygame.draw import *
from math import *

pg.init()

FPS = 30
screen = pg.display.set_mode((400, 400))
def rotate_rect(x, y, a, b, alf, color):
    polygon(screen, color, [(x, y), (x+a*cos(alf), y+a*sin(alf)),
                            (x+a*cos(alf)-b*sin(alf), y+a*sin(alf)+b*cos(alf)),
                            (x-b*sin(alf), y+b*cos(alf)), (x, y)])
rect(screen, (100, 100, 100), (0, 0, 400, 400))
circle(screen, (255, 255, 0), (150, 150), 100)
circle(screen, (255, 0, 0), (112.5, 120), 30)
circle(screen, (255, 0, 0), (300-112.5, 120), 25)
circle(screen, (0, 0, 0), (112.5, 120), 15)
circle(screen, (0, 0, 0), (300-112.5, 120), 15)
rect(screen, (0, 0, 0), (105, 200, 100, 20))
rotate_rect(80, 50, 80, 15, pi/6, (0, 0, 0))
rotate_rect(160, 100, 60, 7, -pi/6, (0, 0, 0))

pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True

pg.quit()
