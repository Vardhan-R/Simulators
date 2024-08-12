import math, pygame, random

pygame.init()

gravity = 0.01
wind = 0
coefficient_of_restitution = 0.9
width = 1400
height = 800
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
all_balls = []
running = True

scrn = pygame.display.set_mode((width, height))
bb = pygame.image.load(r"C:/Users/vrdhn/Desktop/clg/Tinkerers' Lab/basketball.png")



class Ball:
    def __init__(self, px, py):
        self.radius = 32
        self.pos_x = px
        self.pos_y = py
        self.vel_x = random.randint(-10, 10) / 10
        self.vel_y = math.sqrt(1 - self.vel_x ** 2)
        # self.clr = random.choice([red, green, blue, yellow, violet])
        self.clr = (255, 128, 0)

    def update(self):
        self.vel_x += wind
        self.vel_y += gravity
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

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
        # pygame.draw.circle(scrn, self.clr, (self.pos_x, self.pos_y), self.radius)
        scrn.blit(bb, (self.pos_x, self.pos_y))



while running:
    scrn.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            all_balls.append(Ball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "a": wind = -0.001
            elif pygame.key.name(event.key) == "d": wind = 0.001

            if pygame.key.name(event.key) == "space":
                for i in all_balls:
                    i.vel_x *= 2
                    i.vel_y *= 2

        if event.type == pygame.KEYUP:
            if pygame.key.name(event.key) in "ad": wind = 0

    for i in all_balls:
        i.update()
        i.checkEdges()
        i.show()

    pygame.display.update()

pygame.quit()
