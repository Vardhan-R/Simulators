import math, pygame, random

n = 5
gravity = 0
wind = 0
damping = 0
allBlocks = []
width = 800
height = 600
canvas = (width, height)
wind_display = 0
grav_display = False
running = True

class Block:
    def __init__(self):
        self.mass = random.randint(40, 60) / 10
        self.size = self.mass ** 2
        self.posX = random.randint(0, width - math.ceil(self.size))
        self.posY = random.randint(0, height - math.ceil(self.size))
        self.velX = random.randint(-5, 5) / 20
        self.velY = random.randint(-5, 5) / 20
        self.clr = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def checkEdges(self):
        if self.posX <= 0:
            self.velX *= damping - 1
            self.posX = 0
        elif self.posX >= width - self.size:
            self.velX *= damping - 1
            self.posX = width - self.size
        if self.posY <= 0:
            self.velY *= damping - 1
            self.posY = 0
        elif self.posY >= height - self.size:
            self.velY *= damping - 1
            self.posY = height - self.size

    def show(self):
        pygame.draw.rect(scrn, self.clr, pygame.Rect(self.posX, self.posY, self.size, self.size))

for i in range(n):
    allBlocks.append(Block())

pygame.init()

scrn = pygame.display.set_mode(canvas)
icon = pygame.image.load(r'C:\Users\Dr. Mrunalini\Desktop\Vardhan\pygame_images\collisions_icon.png')
wind_lt_img = pygame.image.load(r'C:\Users\Dr. Mrunalini\Desktop\Vardhan\pygame_images\wind_lt_24_px.png')
wind_rt_img = pygame.image.load(r'C:\Users\Dr. Mrunalini\Desktop\Vardhan\pygame_images\wind_rt_24_px.png')
grav_img = pygame.image.load(r'C:\Users\Dr. Mrunalini\Desktop\Vardhan\pygame_images\gravity_24_px.png')

pygame.display.set_icon(icon)
pygame.display.set_caption("Collisions")

while running:
    scrn.fill((0, 0, 0))
    if grav_display:
        scrn.blit(grav_img, (0, 0))
    if wind_display < 0:
        if grav_display:
            scrn.blit(wind_lt_img, (0, 24))
        else:
            scrn.blit(wind_lt_img, (0, 0))
    elif wind_display > 0:
        if grav_display:
            scrn.blit(wind_rt_img, (0, 24))
        else:
            scrn.blit(wind_rt_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "a":
            wind = -0.0001
            wind_display = -1
        elif event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "d":
            wind = 0.0001
            wind_display = 1
        elif event.type == pygame.KEYUP and pygame.key.name(event.key) in "ad":
            wind = 0
            wind_display = 0

        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "space":
            gravity = 0.0001
            grav_display = True
        elif event.type == pygame.KEYUP and pygame.key.name(event.key) == "space":
            gravity = 0
            grav_display = False

    for i in allBlocks:
        i.velX += wind
        i.velY += gravity
        i.posX += i.velX
        i.posY += i.velY
        i.checkEdges()

    for m in range(len(allBlocks)):
        i = allBlocks[m]
        for j in allBlocks[m:]:
            if i != j:
                tempX = i.posX + i.size / 2 - j.posX - j.size / 2
                tempY = i.posY + i.size / 2 - j.posY - j.size / 2
                if abs(tempX) <= (i.size + j.size) / 2 and abs(tempY) <= (i.size + j.size) / 2:
                    if abs(tempX) < abs(tempY):
                        iTempVel, jTempVel = i.velX, j.velX
                        i.velX = (1 - damping) * ((i.mass - j.mass) * iTempVel + 2 * j.mass * jTempVel) / (i.mass + j.mass)
                        j.velX = (1 - damping) * ((j.mass - i.mass) * jTempVel + 2 * i.mass * iTempVel) / (i.mass + j.mass)
                    elif abs(tempX) > abs(tempY):
                        iTempVel, jTempVel = i.velY, j.velY
                        i.velY = (1 - damping) * ((i.mass - j.mass) * iTempVel + 2 * j.mass * jTempVel) / (i.mass + j.mass)
                        j.velY = (1 - damping) * ((j.mass - i.mass) * jTempVel + 2 * i.mass * iTempVel) / (i.mass + j.mass)
                    else:
                        iTempVel, jTempVel = i.velX, j.velX
                        i.velX = (1 - damping) * ((i.mass - j.mass) * iTempVel + 2 * j.mass * jTempVel) / (i.mass + j.mass)
                        j.velX = (1 - damping) * ((j.mass - i.mass) * jTempVel + 2 * i.mass * iTempVel) / (i.mass + j.mass)
                        iTempVel, jTempVel = i.velY, j.velY
                        i.velY = (1 - damping) * ((i.mass - j.mass) * iTempVel + 2 * j.mass * jTempVel) / (i.mass + j.mass)
                        j.velY = (1 - damping) * ((j.mass - i.mass) * jTempVel + 2 * i.mass * iTempVel) / (i.mass + j.mass)
                    i.clr = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                    j.clr = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    for i in allBlocks:
        i.show()

    pygame.display.update()

pygame.quit()
quit()