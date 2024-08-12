import math, pygame, random, time

pygame.init()

width = 800
height = 600
running = True
black = (0, 0, 0)
dark_grey = (64, 64, 64)
grey = (128, 128, 128)
light_grey = (191, 191, 191)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 175, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
orange = (255, 128, 0)
r = 10
g = 0.01
px = width / 2
py = 100
vx = 0
vy = 0
damping = 0.01

class Vector:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

def cuttingPt(pt1, pt2, r): return Vector(r * pt2.x + (1 - r) * pt1.x, r * pt2.y + (1 - r) * pt1.y)

def connect(surface, clr, pts, close = False):
    for m in range(len(pts) - 1): pygame.draw.line(surface, clr, (pts[m].x, pts[m].y), (pts[m + 1].x, pts[m + 1].y))
    if close: pygame.draw.line(surface, clr, (pts[-1].x, pts[-1].y), (pts[0].x, pts[0].y))

pts = []
final_pts = []
c = 1000
ctrl_pts = 8

for i in range(ctrl_pts):
    pts.append(Vector(i * width / (ctrl_pts - 1), random.randint(height / 3, height)))

for i in range(c + 1):
    temp_pts = []
    for j in range(len(pts) - 1): temp_pts.append(cuttingPt(pts[j], pts[j + 1], i / c))
    while len(temp_pts) != 1:
        for j in range(len(temp_pts) - 1): temp_pts[j] = cuttingPt(temp_pts[j], temp_pts[j + 1], i / c)
        temp_pts.pop()

    final_pts.append(temp_pts[0])
    time.sleep(0.005)

scrn = pygame.display.set_mode((width, height))

while running:
    scrn.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    vy += g
    px += vx
    py += vy
    vx *= 1 - damping
    vy *= 1 - damping

    if py + r > final_pts[round(px * c / width)].y:
        if final_pts[round(px * c / width) - 1].y < final_pts[round(px * c / width) + 1].y:
            vx += 1
            py = final_pts[round(px * c / width) + 1].y - r
        elif final_pts[round(px * c / width) - 1].y > final_pts[round(px * c / width) + 1].y:
            vx -= 1
            py = final_pts[round(px * c / width) - 1].y - r
        else:
            py = final_pts[round(px * c / width)].y - r

    pygame.draw.circle(scrn, (200, 0, 0), (px, py), r)
    # connect(scrn, blue, pts)
    for i in range(len(final_pts)):
        pygame.draw.line(scrn, dark_green, (final_pts[i].x, height), (final_pts[i].x, final_pts[i].y))
    # connect(scrn, green, final_pts)

    pygame.display.update()

pygame.quit()