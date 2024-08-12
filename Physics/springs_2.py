from built_modules import import_vectors as vect
from manim import *
import math, pygame, random, time

pygame.init()

width = 800
height = 600
running = True
n = 3
k = 0.01
l_0 = 70
dt = 0.01
all_circles = []
all_horizontal_springs = []
all_vertical_springs = []

class Circle:
    def __init__(self, mass: float | int, radius: float | int, colour: tuple, position: tuple, velocity: tuple = (0, 0)):
        self.m = mass
        self.r = radius
        self.clr = colour
        self.pos = vect.Vector(position[0], position[1])
        self.vel = vect.Vector(velocity[0], velocity[1])
        self.acc = vect.Vector(0, 0)

    def show(self, surface):
        pygame.draw.circle(surface, self.clr, (self.pos.x, self.pos.y), self.r)

scrn = pygame.display.set_mode((width, height))

# all_circles = [[Circle(1, 5, (255, 0, 0), (300 + 50 * j, 200 + 50 * i)) for j in range(n)] for i in range(n)]
# all_circles = [[Circle(1, 5, (255, 0, 0), (random.randrange(0, width), random.randrange(0, height))) for j in range(n)] for i in range(n)]
all_circles = [[Circle(1, 5, (255, 0, 0), (300, 200), (0, 0)), Circle(1, 5, (255, 0, 0), (400, 200), (0, 2)), Circle(1, 5, (255, 0, 0), (500, 200), (0, 0))],
               [Circle(1, 5, (255, 0, 0), (300, 300), (2, 0)), Circle(1, 5, (255, 0, 0), (400, 300), (0, 0)), Circle(1, 5, (255, 0, 0), (500, 300), (-2, 0))],
               [Circle(1, 5, (255, 0, 0), (300, 400), (0, 0)), Circle(1, 5, (255, 0, 0), (400, 400), (0, -2)), Circle(1, 5, (255, 0, 0), (500, 400), (0, 0))]]
all_horizontal_springs = [[0 for j in range(n - 1)] for i in range(n - 1)]
all_vertical_springs = [[0 for j in range(n - 1)] for i in range(n - 1)]
# for i in range(n):
#     temp = []
#     for j in range(n):
#         temp.append(Circle(1, 5, (255, 0, 0), (200 + 50 * j, 200 + 50 * i)))
#         if i and j:
#             all_springs.append(((i - 1, j - 1), (i, j)))
#     all_circles.append(temp)

while running:
    scrn.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(n - 1): # row
        for j in range(n - 1): # col
            temp = vect.sub(all_circles[i][j + 1].pos, all_circles[i][j].pos)
            temp_mag = l_0 / temp.mag()
            all_circles[i][j].acc = vect.add(all_circles[i][j].acc, temp.mult(k * (1 - temp_mag) / all_circles[i][j].m))
            all_circles[i][j + 1].acc = vect.add(all_circles[i][j + 1].acc, temp.mult(-k * (1 - temp_mag) / all_circles[i][j + 1].m))
            all_horizontal_springs[i][j] = temp.mag()

            temp = vect.sub(all_circles[i + 1][j].pos, all_circles[i][j].pos)
            temp_mag = l_0 / temp.mag()
            all_circles[i][j].acc = vect.add(all_circles[i][j].acc, temp.mult(k * (1 - temp_mag) / all_circles[i][j].m))
            all_circles[i + 1][j].acc = vect.add(all_circles[i + 1][j].acc, temp.mult(-k * (1 - temp_mag) / all_circles[i + 1][j].m))
            all_vertical_springs[i][j] = temp.mag()

        temp = vect.sub(all_circles[-1][i + 1].pos, all_circles[-1][i].pos)
        temp_mag = l_0 / temp.mag()
        all_circles[-1][i].acc = vect.add(all_circles[-1][i].acc, temp.mult(k * (1 - temp_mag) / all_circles[-1][i].m))
        all_circles[-1][i + 1].acc = vect.add(all_circles[-1][i + 1].acc, temp.mult(-k * (1 - temp_mag) / all_circles[-1][i + 1].m))
        all_horizontal_springs[-1][i] = temp_mag

        temp = vect.sub(all_circles[i + 1][-1].pos, all_circles[i][-1].pos)
        temp_mag = l_0 / temp.mag()
        all_circles[i][-1].acc = vect.add(all_circles[i][-1].acc, temp.mult(k * (1 - temp_mag) / all_circles[i][-1].m))
        all_circles[i + 1][-1].acc = vect.add(all_circles[i + 1][-1].acc, temp.mult(-k * (1 - temp_mag) / all_circles[i + 1][-1].m))
        all_vertical_springs[i][-1] = temp_mag

        # all_horizontal_springs[-1][i] = vect.sub(all_circles[-1][i].pos, all_circles[-1][i + 1].pos).mag()
        # all_vertical_springs[i][-1] = vect.sub(all_circles[i][-1].pos, all_circles[i + 1][-1].pos).mag()

    for i in range(n):
        for j in range(n):
            all_circles[i][j].vel = vect.add(all_circles[i][j].vel, all_circles[i][j].acc.mult(dt))
            all_circles[i][j].pos = vect.add(all_circles[i][j].pos, all_circles[i][j].vel.mult(dt))
            all_circles[i][j].show(scrn)
            all_circles[i][j].acc = vect.Vector(0, 0)

    for i in range(n - 1):
        for j in range(n - 1):
            temp_1 = all_circles[i][j].pos
            temp_2 = all_circles[i][j + 1].pos
            pygame.draw.line(scrn, (255, 255, 255), (temp_1.x, temp_1.y), (temp_2.x, temp_2.y))
            temp_2 = all_circles[i + 1][j].pos
            pygame.draw.line(scrn, (255, 255, 255), (temp_1.x, temp_1.y), (temp_2.x, temp_2.y))

        temp_1 = all_circles[-1][i].pos
        temp_2 = all_circles[-1][i + 1].pos
        pygame.draw.line(scrn, (255, 255, 255), (temp_1.x, temp_1.y), (temp_2.x, temp_2.y))
        temp_1 = all_circles[i][-1].pos
        temp_2 = all_circles[i + 1][-1].pos
        pygame.draw.line(scrn, (255, 255, 255), (temp_1.x, temp_1.y), (temp_2.x, temp_2.y))

    pygame.display.update()

pygame.quit()

# calc distances
# calc forces
# update velocities
# update positions