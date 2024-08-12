import math, pygame, random, time

pygame.init()

width = 600
height = 600
running = True
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
orange = (255, 128, 0)
clrs = [green, yellow, violet, orange]

class Vector:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

def add(v1, v2): return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sub(v1, v2): return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def mult(k, v): return Vector(k * v.x, k * v.y, k * v.z)

def div(k, v): return Vector(v.x / k, v.y / k, v.z / k)

def dot(v1, v2): return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def cross(v1, v2): return Vector(det([[v1.y, v1.z], [v2.y, v2.z]]), det([[v1.x, v1.z], [v2.x, v2.z]]), det([[v1.x, v1.y], [v2.x, v2.y]]))

def det(t):
    if len(t) > 2:
        s = 0
        for m in range(len(t)):
            p = []
            for n in t:
                p.append(n.copy())
            p.pop(0)
            for n in range(len(p)):
                p[n].pop(m)
            s += (-1) ** m * t[0][m] * det(p)
        return s
    elif len(t) == 2: return t[0][0] * t[1][1] - t[0][1] * t[1][0]
    elif len(t) == 1: return t[0][0]
    else: return 0

def cuttingPt(pt1, pt2, r): return Vector(r * pt2.x + (1 - r) * pt1.x, r * pt2.y + (1 - r) * pt1.y)

def connect(surface, clr, pts, close = False):
    for m in range(len(pts) - 1): pygame.draw.line(surface, clr, (pts[m].x, pts[m].y), (pts[m + 1].x, pts[m + 1].y))
    if close: pygame.draw.line(surface, clr, (pts[-1].x, pts[-1].y), (pts[0].x, pts[0].y))

pts = [Vector(100, 200), Vector(300, 250), Vector(350, 400), Vector(450, 150), Vector(500, 350), Vector(250, 410)]
# pts = [Vector(100, 200), Vector(200, 300), Vector(300, 200)]
final_pts = []
r = 0
c = 1000
done = False

scrn = pygame.display.set_mode((width, height))


while running:
    scrn.fill(black)
    connect(scrn, blue, pts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not(done):
        all_pts = []
        temp_pts = []
        for i in range(len(pts) - 1): temp_pts.append(cuttingPt(pts[i], pts[i + 1], r / c))
        while len(temp_pts) != 1:
            all_pts.append(temp_pts.copy())
            for i in range(len(temp_pts) - 1): temp_pts[i] = cuttingPt(temp_pts[i], temp_pts[i + 1], r / c)
            temp_pts.pop()

        all_pts.reverse()
        final_pts.append(temp_pts[0])
        for i in range(len(all_pts)): connect(scrn, clrs[i], all_pts[i])

    connect(scrn, red, final_pts)
    pygame.display.update()
    time.sleep(0.01)

    if r == c: done = True
    r += 1

pygame.quit()