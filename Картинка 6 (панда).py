import pygame as pg
from pygame.draw import *
from math import *

pg.init()
FPS = 15
screen = pg.display.set_mode((1200, 700))

def ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pg.Rect(rect)
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pg.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def rotate_rect(color, x, y, a, b, alf):
    polygon(screen, color, [(x, y), (x+a*cos(alf), y+a*sin(alf)),
                            (x+a*cos(alf)-b*sin(alf), y+a*sin(alf)+b*cos(alf)),
                            (x-b*sin(alf), y+b*cos(alf)), (x, y)])

screen.fill((255, 180, 140))
def bamboo(x, y, sizex, sizey):
    rect(screen, (0, 125, 0), (x, y, 25*sizex, 70*sizey))
    rect(screen, (0, 125, 0), (x, y-100*sizey, 25*sizex, 90*sizey))
    rotate_rect((0, 125, 0), x+18*sizex, y-170*sizey, 19*sizex, 60*sizey, pi/9*sizex/sizey)
    rotate_rect((0, 125, 0), x + 45 * sizex, y - 255 * sizey, 12 * sizex, 80 * sizey, pi / 9 * sizex / sizey)

    arc(screen, (0, 125, 0),(x+25*sizex, y-140*sizey, 150*sizex, 225*sizey), pi/3, 2*pi/3+0.5, 2)
    arc(screen, (0, 125, 0), (x - 145 * sizex, y - 110 * sizey, 170 * sizex, 250 * sizey), pi / 3- 0.5, 2 * pi / 3-0.1, 2 )

    arc(screen, (0, 125, 0), (x + 38 * sizex, y - 230 * sizey, 350 * sizex, 125 * sizey), pi/2+0.1, pi-0.15, 2)
    arc(screen, (0, 125, 0), (x - 350 * sizex, y - 200 * sizey, 350 * sizex, 140 * sizey), 0.1, pi/2-0.05, 2)

    ellipse_angle(screen, (0, 125, 0), (x-90* sizex, y-110* sizey, 12* sizex, 50* sizey), -20)
    ellipse_angle(screen, (0, 125, 0), (x - 70 * sizex, y - 110 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x - 48 * sizex, y - 100 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)

    ellipse_angle(screen, (0, 125, 0), (x + 100 * sizex, y - 140 * sizey, 10 * sizex, 50 * sizey), 20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x + 120 * sizex, y - 140 * sizey, 10 * sizex, 50 * sizey), 20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x +80 * sizex, y - 130 * sizey, 10 * sizex, 50 * sizey), 20* sizex / sizey)

    ellipse_angle(screen, (0, 125, 0), (x - 150 * sizex, y - 197 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x - 130 * sizex, y - 197 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x - 110 * sizex, y - 192 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x - 90 * sizex, y - 188 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x - 60 * sizex, y - 177 * sizey, 10 * sizex, 50 * sizey), -20* sizex / sizey)

    ellipse_angle(screen, (0, 125, 0), (x + 180 * sizex, y - 227 * sizey, 10 * sizex, 50 * sizey), 20 * sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x + 160 * sizex, y - 227 * sizey, 10 * sizex, 50 * sizey), 20 * sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x + 140 * sizex, y - 222 * sizey, 10 * sizex, 50 * sizey), 20 * sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x + 120 * sizex, y - 218 * sizey, 10 * sizex, 50 * sizey), 20 * sizex / sizey)
    ellipse_angle(screen, (0, 125, 0), (x + 90 * sizex, y - 207 * sizey, 10 * sizex, 50 * sizey), 20 * sizex / sizey)


bamboo(600, 400, 1.25, 1.25)
bamboo(450, 450, 0.45*1.25, 0.75*1.25)


pg.display.update()
clock = pg.time.Clock()
fina = False

while not fina:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fina = True

pg.quit()
