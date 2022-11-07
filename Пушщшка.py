import math
from random import choice
from random import randint
from math import *

import pygame as pg


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
counter = 0
shots_counter = 0

WIDTH = 800
HEIGHT = 600

def rotate_rect(scr, x, y, a, b, alf, color):
    pg.draw.polygon(scr, color, [(x, y), (x+a*cos(alf), y+a*sin(alf)),
                            (x+a*cos(alf)-b*sin(alf), y+a*sin(alf)+b*cos(alf)),
                            (x-b*sin(alf), y+b*cos(alf)), (x, y)])

class Ball(): ####################DONE
    def __init__(self, screen: pg.Surface, x=20, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += 0.98
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r+obj.r)**2:
            return 1
        else: return 0


class Gun:   ####################DONE
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * cos(self.an)
        new_ball.vy = self.f2_power * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] !=20:
                self.an = atan((event.pos[1]-450) / (event.pos[0]-20))
            else:self.an = -pi/2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self): #Добавил индикатор уровня зарядки
        rotate_rect(self.screen, 20, 450, 15, 100, -pi / 2 + self.an, GREY)
        rotate_rect(self.screen, 20, 450, 15, self.f2_power, -pi/2 + self.an, self.color)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.screen = screen
    def oneshot(self):
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 25)
        self.color = RED


    def hit(self, points=0):
        """Попадание шарика в цель."""
        self.points += points
        return self.points

    def draw(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pg.time.Clock()
gun = Gun(screen)
target = Target()
target.live = 0
finished = False

while not finished:
    if not target.live:
        target.oneshot()
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pg.display.update()

    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pg.MOUSEBUTTONUP:
            gun.fire2_end(event)
            shots_counter += 1
        elif event.type == pg.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            counter += target.hit()
            shots_counter = 0
            target.oneshot()
    gun.power_up()

pg.quit()
print(counter)