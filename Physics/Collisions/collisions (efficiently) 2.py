from built_modules import import_vectors as vect
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

class Circle:
    def __init__(self, r, pos, vel):
        self.radius = r
        self.pos = vect.Vector(pos[0], pos[1])
        self.vel = vect.Vector(vel[0], vel[1])

    def updatePos(self):
        self.pos = vect.add(self.pos, self.vel)

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

    if (vect.sub(b.pos, a.pos).mag() <= a.radius + b.radius):
        m1 = a.radius ** 2
        m2 = b.radius ** 2
        dist = vect.sub(b.pos, a.pos)
        parallelCompA = dist.setMag(vect.dot(dist.normalise(), a.vel))
        perpCompA = vect.sub(a.vel, parallelCompA)
        parallelCompB = dist.setMag(vect.dot(dist.normalise(), b.vel))
        perpCompB = vect.sub(b.vel, parallelCompB)
        v1 = vect.add(parallelCompA.mult(m1 - cor * m2), parallelCompB.mult(m2 * (cor + 1))).mult(1 / (m1 + m2))
        v2 = vect.add(parallelCompB.mult(m2 - cor * m1), parallelCompA.mult(m1 * (cor + 1))).mult(1 / (m1 + m2))
        a.vel = vect.add(perpCompA, v1)
        b.vel = vect.add(perpCompB, v2)

all_circles = []
for i in range(300):
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
times = []
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

    a = time.time()

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

    times.append(time.time() - a)

    pygame.display.update()
    # if not(t % 100):
    #     print(c)
    #     t = 0
    # t += 1
    # c = 0

pygame.quit()

print(sum(times) / len(times))