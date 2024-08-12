import math, matplotlib.pyplot as plt, pygame, random, time

pygame.init()

width = 800
height = 600
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
running = True
cor = 1
v_max = 50
a = 100
t = 0
all_circles = []
lst = []

scrn = pygame.display.set_mode((width, height))

class Vector:
	def __init__(self, x, y, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def mult(self, a):
		return Vector(a * self.x, a * self.y, a * self.z)

	def mag(self):
		return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

	def magSq(self):
		return self.x ** 2 + self.y ** 2 + self.z ** 2

	def normalise(self):
		if self.mag() != 0:
			return self.mult(1 / self.mag())

	def setMag(self, m):
		return Vector(self.x / self.mag(), self.y / self.mag(), self.z / self.mag()).mult(m)

	def dir(self): # z = 0
		return(math.atan2(self.y, self.x))

	def setDir(self, t): # z = 0
		return Vector(self.mag() * math.cos(t), self.mag() * math.sin(t), self.z)

	def rotate(self, t): # z = 0
		return Vector(self.mag() * math.cos(self.dir() + t), self.mag() * math.sin(self.dir() + t), self.z)

def vectorAdd(a, b):
	return Vector(a.x + b.x, a.y + b.y, a.z + b.z)

def vectorSub(a, b):
	return Vector(a.x - b.x, a.y - b.y, a.z - b.z)

def vectorDot(a, b):
	return a.x * b.x + a.y * b.y + a.z * b.z

def vectorCross(a, b):
	return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def vectorDistBetween(a, b):
	return Vector(a.x - b.x, a.y - b.y, a.z - b.z).mag()

def vectorAngBetween(a, b):
	return math.acos(vectorDot(a, b) / (a.mag() * b.mag()))

class Circle:
	def __init__(self, r, px, py, vx, vy, clr):
		self.radius = r
		self.pos = Vector(px, py)
		self.vel = Vector(vx, vy)
		self.clr = clr

	def updatePos(self):
		self.pos = vectorAdd(self.pos, self.vel)

	def checkEgdes(self):
		if self.pos.x <= self.radius:
			self.vel.x *= -cor
			self.pos.x = self.radius
		elif self.pos.x >= width - self.radius:
			self.vel.x *= -cor
			self.pos.x = width - self.radius
		if self.pos.y <= self.radius:
			self.vel.y *= -cor
			self.pos.y = self.radius
		elif self.pos.y >= height - self.radius:
			self.vel.y *= -cor
			self.pos.y = height - self.radius

	def show(self):
		pygame.draw.circle(scrn, self.clr, (self.pos.x, self.pos.y), self.radius)

def collision(a, b, v_threshold, n1, n2, rxn):
	global all_circles
	if (vectorSub(b.pos, a.pos).mag() <= a.radius + b.radius):
		dist = vectorSub(b.pos, a.pos)
		parallelCompA = dist.setMag(vectorDot(dist.normalise(), a.vel))
		parallelCompB = dist.setMag(vectorDot(dist.normalise(), b.vel))
		m1 = a.radius ** 2
		m2 = b.radius ** 2
		# print(vectorSub(parallelCompA, parallelCompB).mag())
		if vectorSub(parallelCompA, parallelCompB).mag() < v_threshold:
			perpCompA = vectorSub(a.vel, parallelCompA)
			perpCompB = vectorSub(b.vel, parallelCompB)
			v1 = vectorAdd(parallelCompA.mult(m1 - cor * m2), parallelCompB.mult(m2 * (cor + 1))).mult(1 / (m1 + m2))
			v2 = vectorAdd(parallelCompB.mult(m2 - cor * m1), parallelCompA.mult(m1 * (cor + 1))).mult(1 / (m1 + m2))
			a.vel = vectorAdd(perpCompA, v1)
			b.vel = vectorAdd(perpCompB, v2)
		elif rxn:
			new_pos = vectorAdd(a.pos, dist.setMag(dist.mag() / 2))
			v_com = vectorAdd(a.vel, b.vel)
			v_com.setMag(v_com.mag() / 2)
			return (Circle(math.sqrt(m1 + m2), new_pos.x, new_pos.y, v_com.x, v_com.y, red), n1, n2)

for i in range(500):
	vx = random.randint(-v_max, v_max) / 100
	# all_circles.append(Circle(20, random.randrange(50, width - 50), random.randrange(50, height - 50), random.randint(-50, 50) / 100, random.randrange(-50, 50) / 100, blue))
	all_circles.append(Circle(2, random.randrange(50, width / 2 - 1), random.randrange(50, height - 50), vx, random.choice([-1, 1]) * math.sqrt(v_max ** 2 / 10000 - vx ** 2), red))

while running:
	scrn.fill(black)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# for i in range(len(all_circles)):
	#     for j in range(i, len(all_circles)):
	#         if i != j:
	#             collision(all_circles[i], all_circles[j], 0.6, i, j, False)

	c = 0 # c ==> count
	for i in all_circles:
		if (i.pos.y <= (height - a) / 2 or i.pos.y >= (height + a) / 2) and width / 2 - i.radius <= i.pos.x <= width / 2 + i.radius:
			i.vel.x *= -1

		i.updatePos()
		i.checkEgdes()
		i.show()

		if not(t % 100) and i.pos.x < width / 2:
			c += 1
	if not(t % 100):
		lst.append(c)
		print(len(lst))
	if t >= 50000:
		running = False
	else:
		t += 1

	pygame.draw.line(scrn, white, (width / 2, 0), (width / 2, (height - a) / 2))
	pygame.draw.line(scrn, white, (width / 2, (height + a) / 2), (width / 2, height))

	pygame.display.update()

pygame.quit()
print(lst)
plt.plot(lst)
plt.ylim(0)
plt.show()
