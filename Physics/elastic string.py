import math, pygame, random, time

pygame.init()

g = 0.001
damping = 0.001
width = 800
height = 600
r = 10
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
white = (255, 255, 255)
running = True

scrn = pygame.display.set_mode((width, height))

class ElasticString:
    def __init__(self, k, l, m, px, py, ix, iy): # i as in initial
        self.k = k
        self.l = l
        self.m = m
        self.p = {"x": px, "y": py}
        self.pos = {"x": ix, "y": iy}
        self.vel = {"x": 0, "y": 0}
        self.acc = {"x": 0, "y": 0}

    def calc(self):
        self.delta_l = {"x": self.pos["x"] - self.p["x"], "y": self.pos["y"] - self.p["y"]}

        if pygame.mouse.get_pressed()[0] and (x - self.pos["x"]) ** 2 + (y - self.pos["y"]) ** 2 < r ** 2:
            self.acc = {"x": 0, "y": 0}
            self.vel = {"x": 0, "y": 0}
            self.pos = {"x": x, "y": y}
        else:
            if self.l - math.sqrt(self.delta_l["x"] ** 2 + self.delta_l["y"] ** 2)  < 0:
                self.clr = red
                self.acc = {"x": -self.k * self.delta_l["x"] / self.m, "y": -self.k * self.delta_l["y"] / self.m + g}
                self.vel["x"] += self.acc["x"]
                self.vel["y"] += self.acc["y"]
                self.vel["x"] *= 1 - damping
                self.vel["y"] *= 1 - damping
            else:
                self.clr = green
                self.acc = {"x": 0, "y": g}
                self.vel["y"] += self.acc["y"]

    def checkEdges(self):
        if self.pos["x"] <= r or self.pos["x"] >= width - r: self.vel["x"] *= -1
        if self.pos["y"] <= r or self.pos["y"] >= height - r: self.vel["y"] *= -1

    def updatePos(self):
        self.pos["x"] += self.vel["x"]
        self.pos["y"] += self.vel["y"]

    def show(self):
        pygame.draw.line(scrn, self.clr, (self.p["x"], self.p["y"]), (self.pos["x"], self.pos["y"]))
        pygame.draw.circle(scrn, black, (self.pos["x"], self.pos["y"]), r)

es = ElasticString(0.001, 200, 100, width / 2, 0, width / 2, 190)

while running:
    scrn.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    x = math.floor(pygame.mouse.get_pos()[0])
    y = math.floor(pygame.mouse.get_pos()[1])
    es.calc()
    es.checkEdges()
    es.updatePos()
    es.show()

    pygame.display.update()

pygame.quit()