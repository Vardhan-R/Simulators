import math, pygame, random, time

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
white = (255, 255, 255)
running = True
all_clrs = [red, green, blue, yellow, violet, white]
all_fireworks = []
gravity = 0.001

scrn = pygame.display.set_mode((width, height))

class Particle:
    def __init__(self, clr, px, py):
        self.r = clr[0]
        self.g = clr[1]
        self.b = clr[2]
        self.pos_x = px
        self.pos_y = py
        self.vel_x = random.randint(-50, 50) / 100
        self.vel_y = random.choice([-1, 1]) * math.sqrt(0.25 - self.vel_x ** 2)
        self.max_health = 1000
        self.health = self.max_health
        self.prev_particles = []

    def update(self):
        self.vel_y += gravity
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.health -= 1
        self.prev_particles.append([self.pos_x, self.pos_y])
        if len(self.prev_particles) > 20: self.prev_particles.pop(0)

    def show(self):
        for m in range(len(self.prev_particles) - 1, -1, -1):
            self.k = max(self.health - 10 * (len(self.prev_particles) - m), 0)
            pygame.draw.circle(scrn, (self.r * self.k / self.max_health, self.g * self.k / self.max_health, self.b * self.k / self.max_health), (self.prev_particles[m][0], self.prev_particles[m][1]), 3)
        pygame.draw.circle(scrn, (self.r * self.health / self.max_health, self.g * self.health / self.max_health, self.b * self.health / self.max_health), (self.pos_x, self.pos_y), 3)

class Firework:
    def __init__(self, px, py):
        self.clr = random.choice(all_clrs)
        self.pos_x = px
        self.pos_y = py
        self.vel_x = random.randint(-2, 2)
        self.vel_y = -math.sqrt(16 - self.vel_x ** 2)
        self.blast_height = random.randint(100, 200)
        self.exploded = False
        self.particles = []

    def update(self, x):
        if x:
            self.pos_x += self.vel_x
            self.pos_y += self.vel_y
        else:
            for m in range(50):
                self.particles.append(Particle(self.clr, self.pos_x, self.pos_y))
            self.exploded = True

    def update_2(self):
        for m in self.particles:
            m.update()
            if m.health > 0: m.show()
            else: self.particles.remove(m)

    def show(self):
        if not(self.exploded): pygame.draw.circle(scrn, self.clr, (self.pos_x, self.pos_y), 5)

while running:
    scrn.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            all_fireworks.append(Firework(x, y))

    for i in all_fireworks:
        if not(i.exploded):
            i.update(i.pos_y > i.blast_height)
        else: i.update_2()
        i.show()

    pygame.display.update()
    time.sleep(0.001)

pygame.quit()