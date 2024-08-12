import pygame, random
import matplotlib.pyplot as plt

l = []
width = 800
height = 600
running = True
r = 10
g = 0.01
px = 100
py = width / 2
vx = 0
vy = 0

def noise():
    global l, height
    l = [random.randint(2 / 3 * height, height) / height]
    for i in range(800):
        a = random.randint(0, 1)
        if a: l.append(min(l[-1] + 1 / height, 1))
        else: l.append(max(0, l[-1] - 1 / height))
##    plt.plot([x for x in range(len(l))], l)
##    plt.show()
noise()

pygame.init()

scrn = pygame.display.set_mode((width, height))

while running:
    scrn.fill((200, 200, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vy += g
    px += vx
    py += vy

    if py + r > l[px] * height:
        if l[px - 1] < l[px + 1]:
            vx += 1
            py = l[px + 1] * height - r
        elif l[px - 1] > l[px + 1]:
            vx -= 1
            py = l[px - 1] * height - r
        else:
            py = l[px] * height - r

    for i in range(len(l) - 1):
        pygame.draw.circle(scrn, (200, 0, 0), (px, py), r)
        pygame.draw.line(scrn, (0, 175, 0), (i, l[i] * height), (i + 1, l[i + 1] * height))
        pygame.draw.line(scrn, (0, 175, 0), (i, l[i] * height), (i, height))

    pygame.display.update()

pygame.quit()
