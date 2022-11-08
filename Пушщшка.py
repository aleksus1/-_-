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
number_of_targets = 4
acseleration = 0.98

WIDTH = 800
HEIGHT = 600

def rotate_rect(scr, x, y, a, b, alf, color):
    pg.draw.polygon(scr, color, [(x, y), (x+a*cos(alf), y+a*sin(alf)),
                            (x+a*cos(alf)-b*sin(alf), y+a*sin(alf)+b*cos(alf)),
                            (x-b*sin(alf), y+b*cos(alf)), (x, y)])

class Ball(): ####################DONE
    def __init__(self, screen: pg.Surface):
        global acseleration
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.acseleration = acseleration
        self.screen = screen
        self.x = gun.gunpos
        self.y = HEIGHT-50
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
        self.vy += self.acseleration
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj, i):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x[i])**2 + (self.y - obj.y[i])**2 <= (self.r+obj.r[i])**2:
            return 1

        else: return 0


class Gun:   ####################DONE
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.gunpos = WIDTH/2

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
        self.an = atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * cos(self.an)
        new_ball.vy = self.f2_power * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def aiming(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[1] < 450:
                self.an = -acos((event.pos[0]-self.gunpos)/sqrt((event.pos[1]-HEIGHT+50)**2+(event.pos[0]-self.gunpos)**2))
            else: self.an = acos((event.pos[0]-self.gunpos)/sqrt((event.pos[1]-HEIGHT+50)**2+(event.pos[0]-self.gunpos)**2))


        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self): #Добавил индикатор уровня зарядки
        rotate_rect(self.screen, self.gunpos, HEIGHT-50, 15, 100, -pi / 2 + self.an, GREY)
        rotate_rect(self.screen, self.gunpos, HEIGHT-50, 15, self.f2_power, -pi/2 + self.an, self.color)

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
        self.x = []
        self.y = []
        self.r = []
        self.velx = []
        self.vely = []
    def oneshot(self):
        self.points = 0
        self.live += 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x.append(randint(100, WIDTH-100))
        self.y.append(randint(100, HEIGHT-150))
        self.r.append(randint(2, 25))
        self.velx.append(randint(-5, 5))
        self.vely.append(randint(-5, 5))
        self.color = RED


    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points = points
        self.x = self.x[:i] + self.x[i+1:]
        self.y = self.y[:i] + self.y[i + 1:]
        self.r = self.r[:i] + self.r[i + 1:]
        return 1

    def draw(self, i):
        self.x[i] += self.velx[i]
        self.y[i] += self.vely[i]
        if self.x[i] < self.r[i] or self.x[i] > WIDTH - self.r[i]:
            self.velx[i] = -self.velx[i]
        if self.y[i] < self.r[i] or self.y[i] > HEIGHT-150 - self.r[i]:
            self.vely[i] = -self.vely[i]
        pg.draw.circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pg.time.Clock()
gun = Gun(screen)
target = Target()
target.live = 0
finished = False
LEFT = False
RIGHT = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    while target.live < number_of_targets:
        target.oneshot()
    for i in range(target.live):
        target.draw(i)
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
            gun.aiming(event)
        elif event.type == pg.KEYDOWN: #Делаю чит на отключение гравитации (не знаю зачем)
            if event.key == pg.K_g and acseleration != 0:
                acseleration = 0
            elif event.key == pg.K_g and acseleration == 0:
                acseleration = 0.98
            elif event.key == pg.K_a:
                LEFT = True
            elif event.key == pg.K_d:
                RIGHT = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                LEFT = False
            if event.key == pg.K_d:
                RIGHT = False


    if LEFT:
        gun.gunpos -= 10
    if RIGHT:
        gun.gunpos += 10

    for b in balls:
        b.move()
        for i in range(number_of_targets):
            if b.hittest(target, i) and target.live>0:
                target.live -= 1
                counter += target.hit()
                shots_counter = 0
                target.oneshot()
                b.vx = 0
                b.x = -20
    gun.power_up()


pg.quit()
print(counter)

