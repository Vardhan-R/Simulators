import math, pygame, random, time

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
running = True
ep = 1 # ep ==> epsilon
s = 20 # s ==> sigma
all_particles = []
radius = 5
damping = 0

scrn = pygame.display.set_mode((width, height))

class Vector:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def mult(self, a):
        return Vector(a * self.x, a * self.y, a * self.z)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def magSq(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalise(self):
        if self.mag() != 0:
            return self.mult(1 / self.mag())

    def setMag(self, m):
        return Vector(self.x / self.mag(), self.y / self.mag(), self.z / self.mag()).mult(m)

    def dir(self): # z = 0
        return(math.atan2(self.y, self.x))

    def setDir(self, t): # z = 0
        return Vector(self.mag() * math.cos(t), self.mag() * math.sin(t), self.z)

    def rotate(self, t): # z = 0
        return Vector(self.mag() * math.cos(self.dir() + t), self.mag() * math.sin(self.dir() + t), self.z)

def vectorAdd(a, b):
    return Vector(a.x + b.x, a.y + b.y, a.z + b.z)

def vectorSub(a, b):
    return Vector(a.x - b.x, a.y - b.y, a.z - b.z)

def vectorDot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def vectorCross(a, b):
    return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def vectorDistBetween(a, b):
    return Vector(a.x - b.x, a.y - b.y, a.z - b.z).mag()

def vectorAngBetween(a, b):
    return math.acos(vectorDot(a, b) / (a.mag() * b.mag()))

class Particle:
    def __init__(self, m, p, v, clr):
        self.mass = m
        self.pos = Vector(p[0], p[1])
        self.vel = Vector(v[0], v[1])
        self.acc = Vector(0, 0)
        self.clr = clr

    def update(self):
        self.vel = vectorAdd(self.vel, self.acc)
        self.vel.mult(1 - damping)
        self.pos = vectorAdd(self.pos, self.vel)

    def show(self):
        pygame.draw.circle(scrn, self.clr, (self.pos.x, self.pos.y), radius)

    def checkEdges(self):
        if self.pos.x - radius <= 0:
            self.vel.x *= damping - 1
            # self.pos.x = radius + 1
        elif self.pos.x + radius >= width:
            self.vel.x *= damping - 1
            # self.pos.x = width - radius - 1
        if self.pos.y - radius <= 0:
            self.vel.y *= damping - 1
            # self.pos.y = radius + 1
        elif self.pos.y + radius >= height:
            self.vel.y *= damping - 1
            # self.pos.y = height - radius - 1

def updateAcc():
    global all_particles
    for i in range(len(all_particles)):
        for j in range(i, len(all_particles)):
            if i != j:
                r = vectorSub(all_particles[j].pos, all_particles[i].pos)
                dist = r.mag()
                try:
                    f_mag = 24 * ep * s ** 6 * (2 * s ** 6 / dist ** 13 - 1 / dist ** 7) # f ==> force
                    all_particles[i].acc = vectorAdd(all_particles[i].acc, r.setMag(-f_mag / all_particles[i].mass))
                    all_particles[j].acc = vectorAdd(all_particles[j].acc, r.setMag(f_mag / all_particles[j].mass))
                except:
                    pass
                    # all_particles[i].pos.x = random.randint(radius, width - radius)
                    # all_particles[i].pos.y = random.randint(radius, height - radius)
                    # all_particles[j].pos.x = random.randint(radius, width - radius)
                    # all_particles[j].pos.y = random.randint(radius, height - radius)
                    # all_particles[i].vel = Vector(0, 0)
                    # all_particles[j].vel = Vector(0, 0)

# all_particles.append(Particle(1, (375, 300), (0, 0), red))
# all_particles.append(Particle(1, (20, 70), (0, 0), green))
# all_particles.append(Particle(1, (425, 300), (0, 0), blue))
for i in range(10):
    # all_particles.append(Particle(10, (random.randrange(radius, width - radius), random.randrange(radius, height - radius)), (random.randint(-5, 5) / 100, random.randint(-5, 5) / 100), red))
    all_particles.append(Particle(10, (random.randrange(radius, width - radius), random.randrange(radius, height - radius)), (0, 0), red))

while running:
    scrn.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    updateAcc()

    for i in all_particles:
        i.update()
        i.checkEdges()
        i.show()

    for i in all_particles:
        i.acc = Vector(0, 0)

    pygame.display.update()

pygame.quit()