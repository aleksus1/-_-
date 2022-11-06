import pygame as pg
from pygame.draw import *
from math import *
from random import randint

pg.init()

FPS = 2
screen = pg.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
counter = 0
misses = 0
number_of_balls = 4
absis = [0 for i in range(number_of_balls)]
ordinate = [0 for i in range(number_of_balls)]
radius = [0 for i in range(number_of_balls)]
repeat = 0
colour = []


def new_ball():  # Рисуем шарик
    global x, y, r, color
    x = randint(100, 1100)
    y = randint(100, 700)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def multipul_balls():  # Рисуем несколько шариков, с возможностью указать их максимальное количество
    global number_of_balls, absis, ordinate, radius, FPS, color
    new_ball()

    colour.append(color)
    absis.append(x)
    ordinate.append(y)
    radius.append(r)


def ball_death(): #Удаляем самый ранее появившийся шарик на экране
    global number_of_balls, absis, ordinate, radius, FPS, colour
    screen.fill(BLACK)
    for i in range(1, number_of_balls):
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])
    absis = absis[1:]
    ordinate = ordinate[1:]
    radius = radius[1:]
    colour = colour[1:]



pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(1000)
    for event in pg.event.get():
        not_miss = False
        if event.type == pg.QUIT:
            finished = True

        elif event.type == pg.MOUSEBUTTONDOWN:  # Событие нажатия мыши
            mousepos = list(event.pos)  # запоминаем координаты мыши в момент нажатия

            for i in range(number_of_balls):
                if (absis[i] - mousepos[0]) ** 2 + (ordinate[i] - mousepos[1]) ** 2 <= radius[i] ** 2:  # Проверка попадания в один из кругов
                    counter += 1  # Подсчёт оков
                    print("Tap")
                    not_miss = True
            if not not_miss:
                print("Miss")
                misses += 1  # Подсчёт промахов`
                not_miss = 0
            if misses == 5: finished = True  # Проигрыш при пяти промахах
    multipul_balls()
    if repeat < number_of_balls: #Проверка наличия на экране необходимого числа шариков(один шарик появляется за одно повторение)
        repeat +=1
        screen.fill(BLACK)
    else:
        ball_death()
        clock.tick(FPS)
    pg.display.update()
print("Your count is", counter)
pg.quit()
