import math, pygame, random, time
import import_vectors as vect

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
running = True
# cor = 1
damping = 0.0001

scrn = pygame.display.set_mode((width, height))

class Spring:
    def __init__(self, k, l_0, m1, m2, p1, p2):
        self.k = k
        self.l_0 = l_0
        self.m1 = m1
        self.m2 = m2
        self.p1 = vect.Vector(p1[0], p1[1])
        self.p2 = vect.Vector(p2[0], p2[1])
        self.v1 = vect.Vector(0, 0)
        self.v2 = vect.Vector(0, 0)

    def update(self):
        x = vect.sub(self.p2, self.p1)
        f = self.k * (self.l_0 - x.mag())
        self.v1 = vect.sub(self.v1, x.setMag(f / self.m1)).mult(1 - damping)
        self.v2 = vect.add(self.v2, x.setMag(f / self.m2)).mult(1 - damping)
        self.p1 = vect.add(self.p1, self.v1)
        self.p2 = vect.add(self.p2, self.v2)
        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            mouse_vect = vect.Vector(mouse_x, mouse_y)
            if vect.sub(mouse_vect, self.p1).mag() < 10:
                self.p1 = mouse_vect
            elif vect.sub(mouse_vect, self.p2).mag() < 10:
                self.p2 = mouse_vect

    def show(self):
        if vect.sub(self.p2, self.p1).mag() <= self.l_0:
            pygame.draw.line(scrn, red, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y))
        else:
            pygame.draw.line(scrn, green, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y))
        pygame.draw.circle(scrn, black, (self.p1.x, self.p1.y), self.m1 ** 2)
        pygame.draw.circle(scrn, black, (self.p2.x, self.p2.y), self.m2 ** 2)

class SpringSystem:
    def __init__(self, k, l_0, m, p, v):
        self.all_k = k
        self.all_l_0 = l_0
        self.all_masses = m
        self.all_pos = []
        self.all_vels = []
        for i in range(len(p)):
            self.all_pos.append(vect.Vector(p[i][0], p[i][1]))
            self.all_vels.append(vect.Vector(v[i][0], v[i][1]))

    def update(self):
        for i in range(len(self.all_k)):
            x = vect.sub(self.all_pos[i + 1], self.all_pos[i])
            f = self.all_k[i] * (self.all_l_0[i] - x.mag())
            if f < 0: # elastic string
                self.all_vels[i] = vect.sub(self.all_vels[i], x.setMag(f / self.all_masses[i])).mult(1 - damping)
                self.all_vels[i + 1] = vect.add(self.all_vels[i + 1], x.setMag(f / self.all_masses[i])).mult(1 - damping)

        for i in range(len(self.all_pos)):
            self.all_pos[i] = vect.add(self.all_pos[i], self.all_vels[i])

        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            mouse_vect = vect.Vector(mouse_x, mouse_y)
            for i in range(len(self.all_pos)):
                if vect.sub(mouse_vect, self.all_pos[i]).mag() < math.sqrt(self.all_masses[i]):
                    self.all_pos[i] = mouse_vect
                    break

    def show(self):
        for i in range(len(self.all_k)):
            if vect.sub(self.all_pos[i + 1], self.all_pos[i]).mag() <= self.all_l_0[i]:
                pygame.draw.line(scrn, green, (self.all_pos[i].x, self.all_pos[i].y), (self.all_pos[i + 1].x, self.all_pos[i + 1].y))
            else:
                pygame.draw.line(scrn, red, (self.all_pos[i].x, self.all_pos[i].y), (self.all_pos[i + 1].x, self.all_pos[i + 1].y))

        for i in range(len(self.all_pos)):
            pygame.draw.circle(scrn, black, (self.all_pos[i].x, self.all_pos[i].y), math.sqrt(self.all_masses[i]))

# spring_1 = Spring(0.0001, 250, 3, 4, (200, height / 2), (600, height / 2))
# spring_system_1 = SpringSystem((0.01, 0.01), (150, 150), (256, 256, 256), ((width / 4, height / 2), (width / 2, height / 2), (3 * width / 4, height / 2)), ((0, 0), (0, 0), (0, 0)))
k = []
l_0 = []
m = []
p = []
v = []
for i in range(-5, 5):
    if i != -5:
        k.append(0.001)
        l_0.append(10)
    m.append(25)
    p.append((width / 2, height / 2 + 10 * i))
    v.append((0, 0))

spring_system_2 = SpringSystem(k, l_0, m, p, v)

while running:
    scrn.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # spring_1.update()
    # spring_1.show()
    # spring_system_1.update()
    # spring_system_1.show()
    spring_system_2.update()
    spring_system_2.show()

    pygame.display.update()

pygame.quit()