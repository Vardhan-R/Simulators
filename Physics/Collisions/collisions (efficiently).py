import math, pygame, random, time

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
running = True
cor = 1
radius = 5
# c = 0
# t = 0

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

    def show(self):
        pygame.draw.circle(scrn, white, (self.pos.x, self.pos.y), self.radius)

def collision(a, b):
    # global c
    # c += 1

    if (vectorSub(b.pos, a.pos).mag() <= a.radius + b.radius):
        m1 = a.radius ** 2
        m2 = b.radius ** 2
        dist = vectorSub(b.pos, a.pos)
        parallelCompA = dist.setMag(vectorDot(dist.normalise(), a.vel))
        perpCompA = vectorSub(a.vel, parallelCompA)
        parallelCompB = dist.setMag(vectorDot(dist.normalise(), b.vel))
        perpCompB = vectorSub(b.vel, parallelCompB)
        v1 = vectorAdd(parallelCompA.mult(m1 - cor * m2), parallelCompB.mult(m2 * (cor + 1))).mult(1 / (m1 + m2))
        v2 = vectorAdd(parallelCompB.mult(m2 - cor * m1), parallelCompA.mult(m1 * (cor + 1))).mult(1 / (m1 + m2))
        a.vel = vectorAdd(perpCompA, v1)
        b.vel = vectorAdd(perpCompB, v2)

all_circles = []
for i in range(100):
    all_circles.append(Circle(radius, (random.randrange(radius, width - radius), random.randrange(radius, height - radius)), (random.randint(-50, 50) / 100, random.randrange(-50, 50) / 100)))

n = len(all_circles)
def f(x):
    return n * ((n - 1) / x + x) / 2
    # return n * ((n - 1) / (2 * x) + x)

x = math.sqrt((n - 1))
# x = math.sqrt((n - 1) / 2)
if f(math.floor(x)) <= f(math.ceil(x)):
    regions = math.floor(x)
else:
    regions = math.ceil(x)

col_width = width / regions # col ==> column
lst = []
for i in range(regions):
    lst.append([])
while running:
    scrn.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # for i in range(len(all_circles)):
    #     for j in range(regions):
    #         if j * col_width - radius < all_circles[i].pos.x < (j + 1) * col_width + radius:
    #             lst[j].append(i)
    #             if (j + 1) * col_width - radius < all_circles[i].pos.x < (j + 2) * col_width + radius:
    #                 lst[j + 1].append(i)
    #                 break

    for i in range(len(all_circles)):
        for j in range(regions):
            if all_circles[i].pos.x < (j + 1) * col_width:
                lst[j].append(i)
                break

    for i in lst:
        for j in range(len(i)):
            for k in range(j, len(i)):
                if j != k:
                    collision(all_circles[i[j]], all_circles[i[k]])
        i.clear()

    for i in range(regions):
        pygame.draw.line(scrn, green, ((i + 1) * col_width, 0), ((i + 1) * col_width, height))

    for i in all_circles:
        i.updatePos()
        i.checkEgdes()
        i.show()

    pygame.display.update()
    # if not(t % 100):
    #     print(c)
    #     t = 0
    # t += 1
    # c = 0

pygame.quit()