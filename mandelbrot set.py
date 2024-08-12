import math, pygame, random, time

pygame.init()

width = 600
height = 600
running = True
density = 150 # higher density ==> more preprocessing time

xl = -3
xr = 1
yd = -2
yu = 2

black = (0, 0, 0)
dark_grey = (85, 85, 85)
light_grey = (170, 170, 170)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
violet = (255, 0, 255)
all_colours = [red, green, blue, yellow, violet]

scrn = pygame.display.set_mode((width, height))
font_size = 16
font = pygame.font.Font("freesansbold.ttf", font_size)

def grid(xl, xr, yd, yu): # xl as in x-left, xr as in x-right, yd as in y-down and yu as in y-up
	for i in range(xl, xr + 1):
		pygame.draw.line(scrn, dark_grey, ((i - xl) * width / (xr - xl), 0), ((i - xl) * width / (xr - xl), height))
		if i:
			text = font.render(str(i), True, white)
			scrn.blit(text, ((i - xl) * width / (xr - xl) - 6, yu * height / (yu - yd) + 2))
	for i in range(yd, yu + 1):
		pygame.draw.line(scrn, dark_grey, (0, (yu - i) * height / (yu - yd)), (width, (yu - i) * height / (yu - yd)))
		if yu + yd - i:
			text = font.render(str(yu + yd - i), True, white)
			scrn.blit(text, (width * xl / (xl - xr) - 14, height * (i - yd) / (yu - yd) - 6))
	pygame.draw.line(scrn, light_grey, (width * xl / (xl - xr), 0), (width * xl / (xl - xr), height), 2)
	pygame.draw.line(scrn, light_grey, (0, height * yu / (yu - yd)), (width, height * yu / (yu - yd)), 2)
	text = font.render("0", True, white)
	scrn.blit(text, (width * xl / (xl - xr) - 10, height * yu / (yu - yd) + 2))

def write(re, im): return str(re) + " + " + str(im) + "i"

class Comp:
	def __init__(self, r, i):
		self.r = r
		self.i = i
		self.z = str(r) + " + " + str(i) + "i"

	def copy(self): return Comp(self.r, self.i)

	def mag(self): return math.sqrt(self.r ** 2 + self.i ** 2)

	def magSq(self): return self.r ** 2 + self.i ** 2

	def normalise(self): return self.write(self.r / self.mag(), self.i / self.mag())

	def setMag(self, m):
		try: return self.write(m * self.r / self.mag(), m * self.i / self.mag())
		except: pass

	def angle(self):
		if math.atan2(self.i, self.r) < 0: return 2 * math.pi + math.atan2(self.i, self.r)
		else: return math.atan2(self.i, self.r)

	def plot(self, clr):
		# pygame.draw.circle(scrn, clr, (width * (xl - self.r) / (xl - xr), height * (yu - self.i) / (yu - yd)), 1)
		x = round(width * (xl - self.r) / (xl - xr))
		y = round(height * (yu - self.i) / (yu - yd))
		scrn.set_at((x, y), clr)

def add(z1, z2): return Comp(z1.r + z2.r, z1.i + z2.i)
def sub(z1, z2): return Comp(z1.r - z2.r, z1.i - z2.i)
def mult(z1, z2): return Comp(z1.r * z2.r - z1.i * z2.i, z1.r * z2.i + z1.i * z2.r)
def root(n, z):
	roots = []
	for k in range(n): roots.append(Comp((z.mag() ** (1 / n)) * math.cos((z.angle() + 2 * math.pi * k) / n), (z.mag() ** (1 / n)) * math.sin((z.angle() + 2 * math.pi * k) / n)))
	return roots

pts = []
for i in range(int(-2.5 * density), int(0.5 * density)):
	for j in range(int(-1.2 * density), int(1.2 * density)):
		c = Comp(i / density, j / density)
		z = Comp(0, 0)
		v = True
		for k in range(100): # max iters to check if the point diverges
			z = add(mult(z, z), c)
			if z.mag() > 2: # it is known that a point which exceeds 2 will certainly diverge
				v = False
				break
		if v: pts.append(c)
	time.sleep(0.01)
	print(i)

while running:
	scrn.fill(black)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	grid(xl, xr, yd, yu)
	for i in pts:
		i.plot(blue)

	pygame.display.update()
