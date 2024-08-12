from built_modules import import_vectors as vect
from manim import *
from perlin_noise import PerlinNoise
import math, pygame, random

pygame.init()

width = 800
height = 600
running = True
n = 100
d_0 = 100
tm = 0
dt = 0.001
rate = 0.002 / n
step_size = 1
# noise = PerlinNoise(octaves = 8)

class Firefly:
    def __init__(self, pos: vect.Vector | None = None, freq: float | int | None = None, phase: float | int | None = None):
        if pos:
            self.pos = pos
        else:
            self.pos = vect.Vector(random.randrange(0, width), random.randrange(0, height))

        # self.vel = vect.Vector(0, 0)

        if freq:
            self.freq = freq
        else:
            self.freq = random.randint(100, 1000) / 100

        if phase:
            self.phase = phase
        else:
            # self.phase = random.randrange(0, round(2 * 10 ** 6 * math.pi)) / 10 ** 6
            self.phase = random.randrange(0, 2 * 10 ** 6) / 10 ** 6

        self.d_freq = 0
        self.d_phase = 0
        self.val = 127 * (math.floor(self.phase) % 2 + 1)
        # self.offset = vect.Vector(random.randint(0, 10 ** 4), random.randint(0, 10 ** 4))

    def calcValue(self, t: float | int):
        self.val = 255 * (math.sin(2 * math.pi * self.freq * t + self.phase) + 1) / 2
        # print(2 / 255 * self.val - 1)
        # self.val = 127 * (math.floor(self.freq * t + self.phase) % 2 + 1)
        # temp = 2 / 255 * self.val - 1
        # if temp > 1:
        #     temp = 1 - temp
        # elif temp < -1:
        #     temp = -(temp + 1)
        # temp = max(temp, -1)
        # temp = min(temp, 1)
        # temp_2 = math.asin(temp)
        # self.val += 255 * math.pi * self.freq * math.cos(temp_2) * dt * temp_2 / abs(temp_2)

    def checkEdges(self):
        if self.pos.x <= 5:
            self.pos.x = 6
        elif self.pos.x >= width - 5:
            self.pos.x = width - 6

        if self.pos.y <= 5:
            self.pos.y = 6
        elif self.pos.y >= height - 5:
            self.pos.y = height - 6

    def show(self):
        # print(self.val)
        pygame.draw.circle(scrn, (0, self.val, 0), (self.pos.x, self.pos.y), 5)

    def update(self, rate: float | int = 1):
        # self.vel.x += step_size * noise(self.offset.x)
        # self.pos.x += step_size * noise(self.offset.x)
        # self.offset.x += 10 ** (-5)
        # self.pos.x += self.vel.x
        # self.vel.y += step_size * noise(self.offset.y)
        # self.pos.y += step_size * noise(self.offset.y)
        # self.offset.y += 10 ** (-5)
        # self.pos.y += self.vel.y
        # self.pos.x += step_size * noise(self.offset.x)
        # self.pos.y += step_size * noise(self.offset.y)
        # self.offset.y += 0.001
        self.freq += rate * self.d_freq
        self.phase += rate * self.d_phase

scrn = pygame.display.set_mode((width, height))

def dist(a: Firefly, b: Firefly):
    return math.sqrt((b.pos.x - a.pos.x) ** 2 + (b.pos.y - a.pos.y) ** 2)

all_fireflies = [Firefly() for _ in range(n)]
# all_fireflies = [Firefly(freq = 5, phase = 0), Firefly(freq = 10, phase = 0)]

while running:
    scrn.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in all_fireflies:
        i.d_freq = 0
        i.d_phase = 0
        i.show()

    for i in range(n - 1):
        for j in range(i + 1, n):
            exp_factor = math.e ** (-dist(all_fireflies[i], all_fireflies[j]) / d_0)
            d_freq = (all_fireflies[j].freq - all_fireflies[i].freq) * exp_factor
            all_fireflies[i].d_freq += d_freq
            all_fireflies[j].d_freq -= d_freq
            d_phase = (all_fireflies[j].phase - all_fireflies[i].phase) * exp_factor
            all_fireflies[i].d_phase += d_phase
            all_fireflies[j].d_phase -= d_phase

        all_fireflies[i].update(rate)
        # all_fireflies[i].checkEdges()
        all_fireflies[i].calcValue(tm)
        # all_fireflies[i].show()

    all_fireflies[n - 1].update(rate)
    # all_fireflies[0].calcValue(tm)
    # all_fireflies[0].show()
    # all_fireflies[n - 1].checkEdges()
    all_fireflies[n - 1].calcValue(tm)
    # all_fireflies[n - 1].show()
    # print(all_fireflies[1].freq - all_fireflies[0].freq)

    tm += dt
    # if (tm >= 1):
    #     tm -= 1

    pygame.display.update()

pygame.quit()