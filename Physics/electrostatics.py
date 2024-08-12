from built_modules import import_vectors as vect
import math, pygame, random, time

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
dark_grey = (64, 64, 64)
grey = (128, 128, 128)
light_grey = (191, 191, 191)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 128, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
orange = (255, 128, 0)
running = True
k = 100
damping = 0
all_particles = []

scrn = pygame.display.set_mode((width, height))

class Particle:
    def __init__(self, m, q, p, v, clr):
        self.m = m
        self.q = q
        self.pos = vect.Vector(p[0], p[1])
        self.vel = vect.Vector(v[0], v[1])
        self.acc = vect.Vector(0, 0)
        self.clr = clr

    def show(self):
        pygame.draw.circle(scrn, self.clr, (self.pos.x, self.pos.y), 10)

def update():
    global all_particles

    for m in range(len(all_particles)):
        for n in range(m, len(all_particles)):
            if m != n:
                r = vect.sub(all_particles[n].pos, all_particles[m].pos)
                try:
                    f = r.setMag(k * all_particles[m].q * all_particles[n].q / r.magSq())
                    all_particles[m].acc = vect.add(all_particles[m].acc, f.mult(-1 / all_particles[m].m))
                    all_particles[n].acc = vect.add(all_particles[n].acc, f.mult(1 / all_particles[n].m))
                except:
                    pass

    for m in all_particles:
        m.vel = vect.add(m.vel, m.acc).mult(1 - damping)
        m.pos = vect.add(m.pos, m.vel)
        m.acc = vect.Vector(0, 0)

all_particles.append(Particle(1, 1, (400, 300), (0, 0), red))
all_particles.append(Particle(1, 1, (300, 400), (0, 0), green))
all_particles.append(Particle(1, 1, (600, 300), (0, 0), blue))

while running:
    scrn.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()

    for i in all_particles:
        i.show()

    pygame.display.update()

pygame.quit()
