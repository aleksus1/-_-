import pygame as pg
from pygame.draw import *
from math import *
from random import randint

pg.init()

FPS = 20
screen = pg.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GOLD = (200, 200, 20)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
counter = 0
misses = 0
number_of_balls = 4
absis = [0 for i in range(number_of_balls)]
ordinate = [0 for i in range(number_of_balls)]
radius = [0 for i in range(number_of_balls)]
velocity = [[0, 0] for i in range(number_of_balls)]
repeat = 0
colour = [0 for i in range(number_of_balls)]
cycle = 0
gold = 0


def new_ball():  # Рисуем шарик
    global x, y, r, color, vx, vy
    x = randint(100, 1100)
    y = randint(100, 700)
    r = randint(5, 100)
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def multiple_balls():  # Рисуем несколько шариков, с возможностью указать их максимальное количество
    global number_of_balls, absis, ordinate, radius, FPS, color, velocity
    new_ball()
    velocity.append([vx, vy])
    colour.append(color)
    absis.append(x)
    ordinate.append(y)
    radius.append(r)


def ball_move():  # Передвижение шариков по экрану
    global number_of_balls, absis, ordinate, radius, FPS, colour, velocity
    screen.fill(BLACK)
    for i in range(number_of_balls):
        absis[i] += velocity[i][0]
        ordinate[i] += velocity[i][1]
        if radius[i] > absis[i]:
            velocity[i][0] = randint(0, 10)
            velocity[i][1] = randint(-10, 10)
        if radius[i] > ordinate[i]:
            velocity[i][1] = randint(0, 10)
            velocity[i][0] = randint(-10, 10)
        if absis[i] > 1200 - radius[i]:
            velocity[i][0] = randint(-10, 0)
            velocity[i][1] = randint(-10, 10)
        if ordinate[i] > 800 - radius[i]:
            velocity[i][1] = randint(-10, 0)
            velocity[i][0] = randint(-10, 10)
        absis[i] += velocity[i][0]
        ordinate[i] += velocity[i][1]
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])


def ball_death(n):  # Удаляем самый ранее появившийся шарик на экране
    global number_of_balls, absis, ordinate, radius, FPS, colour, velocity
    screen.fill(BLACK)
    velocity = velocity[:n] + velocity[n + 1:]
    absis = absis[:n] + absis[n + 1:]
    ordinate = ordinate[:n] + ordinate[n + 1:]
    radius = radius[:n] + radius[n + 1:]
    colour = colour[:n] + colour[n + 1:]
    for i in range(number_of_balls - 1):
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])


def golden_move():
    global vx_gold, vy_gold, x_gold, y_gold
    x_gold += vx_gold
    y_gold += vy_gold
    vx_gold = randint(-40, 40)
    vy_gold = randint(-40, 40)
    rect(screen, GOLD, (x_gold, y_gold, 40, 40))
    pg.display.update()


def golden_rect():
    global x_gold, y_gold, vx_gold, vy_gold
    x_gold = randint(100, 1100)
    y_gold = randint(100, 700)
    vx_gold = randint(-100, 100)
    vy_gold = randint(-100, 100)
    rect(screen, GOLD, (x_gold, y_gold, 25, 25))


def score_points(rad, vel):  # Подсчёт очков за различные цели(с учётом размера и скорости)
    global counter
    if rad > 50:
        precounter = 1
    elif rad > 30:
        precounter = 2
    elif rad > 15:
        precounter = 4
    else:
        precounter = 8
    if sqrt(vel) < 5:
        counter += precounter
    elif sqrt(vel) <= 8:
        counter += precounter * 2
    elif sqrt(vel) <= 12:
        counter += precounter * 4
    elif sqrt(vel) <= 15:
        counter += precounter * 8


pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    multiple_balls()

    if cycle < 20:  # Реализуем движение шариков
        clock.tick(FPS)
        ball_move()
        pg.display.update()
        cycle += 1
    else:
        ball_death(0)  # Реализуем удаление шариков по истечении их срока жизни
        pg.display.update()
        cycle = 0

    for event in pg.event.get():
        not_miss = False
        if event.type == pg.QUIT:
            finished = True

        elif event.type == pg.MOUSEBUTTONDOWN:  # Событие нажатия мыши
            mousepos = list(event.pos)  # запоминаем координаты мыши в момент нажатия

            for i in range(number_of_balls):
                if (absis[i] - mousepos[0]) ** 2 + (ordinate[i] - mousepos[1]) ** 2 <= radius[i] ** 2:  # Проверка попадания в один из кругов
                    score_points(radius[i], velocity[i][0] ** 2 + velocity[i][1] ** 2)  # Подсчёт оков
                    print("Tap")
                    not_miss = True
                    ball_death(i)  # Удаление нажатого шарика
                    pg.display.update()
            if gold > 0:
                if abs(x_gold - mousepos[0]) <= 25 or abs(y_gold - mousepos[1]) <= 25:
                    print("Mega Tap")
                    not_miss = True
                    counter += 100
                    gold = 0
            if not not_miss:
                print("Miss")
                misses += 1  # Подсчёт промахов
                not_miss = 0
            if misses == 5:
                finished = True  # Проигрыш при пяти промахах
                print("You lose!!!")

    if randint(0, 150) == 13 and gold == 0:
        golden_rect()
        gold = 50
    if gold > 0:
        golden_move()
        gold -= 1

print("Your score is", counter)
pg.quit()
