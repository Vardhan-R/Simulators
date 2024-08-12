from import_vectors import *
from manim import *
import math, pygame, random, time

pygame.init()

width = 600
height = 600
running = True
cor = 1
radius = 5

class Circle:
    def __init__(self, r, pos, vel):
        self.radius = r
        self.pos = Vector(pos[0], pos[1])
        self.vel = Vector(vel[0], vel[1])

    def updatePos(self):
        self.pos = vectorAdd(self.pos, self.vel)

    def checkEgdes(self):
        if self.pos.x <= self.radius:
            self.vel.x *= -cor
            self.pos.x = self.radius
        elif self.pos.x >= width - self.radius:
            self.vel.x *= -cor
            self.pos.x = width - self.radius
        if self.pos.y <= self.radius:
            self.vel.y *= -cor
            self.pos.y = self.radius
        elif self.pos.y >= height - self.radius:
            self.vel.y *= -cor
            self.pos.y = height - self.radius

scrn = pygame.display.set_mode((width, height))