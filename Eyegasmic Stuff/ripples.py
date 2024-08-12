import pygame, random

pygame.init()

width = 1440
height = 900
running = True

class Ripple:
    def __init__(self):
        self.pos = (random.randrange(0, width), random.randrange(0, height))
        self.lifespan = random.randint(50, 300)
        self.age = 0
        self.clr = [0, 0, 0]

scrn = pygame.display.set_mode((width, height))

all_ripples = [Ripple()]

while running:
    scrn.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not random.randrange(0, 300):
        all_ripples.append(Ripple())

    for i in range(len(all_ripples) - 1, -1, -1):
        all_ripples[i].age += 0.1
        temp = all_ripples[i].age / all_ripples[i].lifespan
        all_ripples[i].clr[0] = 135 * temp
        all_ripples[i].clr[1] = 206 * temp
        all_ripples[i].clr[2] = 235 * temp
        if all_ripples[i].age >= all_ripples[i].lifespan:
            all_ripples.pop(i)
        else:
            pygame.draw.circle(scrn, all_ripples[i].clr, all_ripples[i].pos, all_ripples[i].age, 1)

    pygame.display.update()

pygame.quit()