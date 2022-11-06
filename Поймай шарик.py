import pygame as pg
from pygame.draw import *
from math import *
from random import randint

pg.init()

FPS =1
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
    r = randint(5, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def multipul_balls():  # Рисуем несколько шариков, с возможностью указать их максимальное количество
    global number_of_balls, absis, ordinate, radius, FPS, color
    new_ball()

    colour.append(color)
    absis.append(x)
    ordinate.append(y)
    radius.append(r)



def ball_death(n): #Удаляем самый ранее появившийся шарик на экране
    global number_of_balls, absis, ordinate, radius, FPS, colour
    screen.fill(BLACK)
    absis = absis[:n] + absis[n+1:]
    ordinate = ordinate[:n] + ordinate[n+1:]
    radius = radius[:n] + radius[n+1:]
    colour = colour[:n] + colour[n+1:]
    for i in range(number_of_balls-1):
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])


def score_points(rad):
    global counter
    if rad>50:
        counter+=1
    elif rad>30: counter+=2
    elif rad>10: counter+=4
    else: counter+=8


pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    clock.tick(1000)

    multipul_balls()
    if repeat < number_of_balls:  # Проверка наличия на экране необходимого числа шариков(один шарик появляется за одно повторение)
        repeat += 1
    else:
        ball_death(0)
        pg.display.update()
        clock.tick(FPS)

    for event in pg.event.get():
        not_miss = False
        if event.type == pg.QUIT:
            finished = True

        elif event.type == pg.MOUSEBUTTONDOWN:  # Событие нажатия мыши
            mousepos = list(event.pos)  # запоминаем координаты мыши в момент нажатия

            for i in range(number_of_balls):
                if (absis[i] - mousepos[0]) ** 2 + (ordinate[i] - mousepos[1]) ** 2 <= radius[i] ** 2:  # Проверка попадания в один из кругов
                    score_points(radius[i])  # Подсчёт оков
                    print("Tap")
                    not_miss = True
                    ball_death(i) #Удаление нажатого шарика
                    multipul_balls()
                    pg.display.update()
            if not not_miss:
                print("Miss")
                misses += 1  # Подсчёт промахов
                not_miss = 0
            if misses == 5: finished = True  # Проигрыш при пяти промахах



print("Your score is", counter)
pg.quit()
