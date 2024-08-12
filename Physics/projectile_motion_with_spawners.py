import math, pygame, random

pygame.init()

gravity = 0.001
wind = 0
coefficient_of_restitution = 0.9
frame_cnt = 0
tm = 10
spd = 0.2
width = 800
height = 600
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
white = (255, 255, 255)
all_spawns = []
all_balls = []
running = True

scrn = pygame.display.set_mode((width, height))



class Ball:
    def __init__(self, px, py):
        self.radius = 2
        self.pos_x = px
        self.pos_y = py
        self.vel_x = random.randint(-100 * spd, 100 * spd) / 100
        self.sign = random.randint(-1, 1)
        while not(self.sign):
            self.sign = random.randint(-1, 1)
        self.vel_y = self.sign * math.sqrt(spd ** 2 - self.vel_x ** 2)
        self.clr = random.choice([red, green, blue, yellow, violet, white])
        self.max_lifespan = 2500
        self.lifespan = self.max_lifespan

    def update(self):
        self.vel_x += wind
        self.vel_y += gravity
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.lifespan -= 1

    def checkEdges(self):
        if self.pos_x <= self.radius:
            self.vel_x *= -coefficient_of_restitution
            self.pos_x = self.radius + 1
        elif self.pos_x >= width - self.radius:
            self.vel_x *= -coefficient_of_restitution
            self.pos_x = width - self.radius - 1
        if self.pos_y <= self.radius:
            self.vel_y *= -coefficient_of_restitution
            self.pos_y = self.radius + 1
        elif self.pos_y >= height - self.radius:
            self.vel_y *= -coefficient_of_restitution
            self.pos_y = height - self.radius - 1

    def show(self):
        pygame.draw.circle(scrn, (self.clr[0] * self.lifespan / self.max_lifespan, self.clr[1] * self.lifespan / self.max_lifespan, self.clr[2] * self.lifespan / self.max_lifespan), (self.pos_x, self.pos_y), self.radius)



while running:
    scrn.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            all_balls.append(Ball(x, y))
            all_spawns.append((x, y))

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "a": wind = -0.001
            elif pygame.key.name(event.key) == "d": wind = 0.001

            if pygame.key.name(event.key) == "space":
                for i in all_balls:
                    i.vel_x *= 2
                    i.vel_y *= 2

        if event.type == pygame.KEYUP:
            if pygame.key.name(event.key) in "ad": wind = 0

    temp_lst = []
    for i in range(len(all_balls)):
        if all_balls[i].lifespan > 0:
            all_balls[i].update()
            all_balls[i].checkEdges()
            all_balls[i].show()
        else:
            temp_lst.append(i)
    for i in temp_lst:
        all_balls.pop(i)

    if not(frame_cnt % tm):
        for i in all_spawns:
            all_balls.append(Ball(i[0], i[1]))
        frame_cnt = 0
    frame_cnt += 1
    pygame.display.update()

pygame.quit()