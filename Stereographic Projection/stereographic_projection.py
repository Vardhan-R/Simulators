from built_modules import import_matrices as mat, import_vectors as vect
from manim import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math, pygame

pygame.init()

width = 800
height = 600
canvas = (width, height)
running = True
clrs = [(1, 0, 0), (0, 0, 1), (1, 0.5, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1)]
prev_key_states = {"w": False, "s": False, "a": False, "d": False, "q": False, "e": False}
res = 16
radius = 3
theta = res
phi = 0
d_theta = 0.25
d_phi = 0.25

pygame.display.set_mode(canvas, pygame.DOUBLEBUF | pygame.OPENGL)

class LatitudeCircle:
	def __init__(self, radius: float | int, angle: float | int):
		# self.centre = (0, radius * math.cos(angle), 0) # y
		self.centre = (0, 0, radius * math.cos(angle)) # z
		self.radius = radius * math.sin(angle)

		self.vertices = []
		self.edges = []
		# for i in range(res): # y
		#     self.vertices.append((self.radius * math.cos(2 * math.pi * i / res), self.centre[1], self.radius * math.sin(2 * math.pi * i / res)))
		#     if i:
		#         self.edges.append((i - 1, i))
		# self.edges.append((res - 1, 0))

		for i in range(res + 1): # z
			self.vertices.append((self.radius * math.cos(math.pi * i / res), self.radius * math.sin(math.pi * i / res), self.centre[2]))
			if i:
				self.edges.append((i - 1, i))

	def show(self):
		glLineWidth(1)
		glBegin(GL_LINES)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.vertices[vertex])
		glEnd()

class LongitudeCircle:
	def __init__(self, radius: float | int, angle: float | int):
		self.centre = (0, 0, 0)
		self.radius = radius

		self.vertices = []
		self.edges = []
		for i in range(res + 1):
			# self.vertices.append((self.radius * math.cos(angle) * math.cos(math.pi * i / res), -self.radius * math.sin(math.pi * i / res), -self.radius * math.sin(angle) * math.cos(math.pi * i / res))) # y
			self.vertices.append((self.radius * math.cos(angle) * math.cos(math.pi * (i / res + 1 / 2)), -self.radius * math.sin(angle) * math.cos(math.pi * (i / res + 1 / 2)), -self.radius * math.sin(math.pi * (i / res + 1 / 2)))) # z
			if i:
				self.edges.append((i - 1, i))
		self.edges.append((res, 0))

	def show(self):
		glLineWidth(1)
		glBegin(GL_LINES)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.vertices[vertex])
		glEnd()

gluPerspective(45, width / height, 0.1, 50)

glTranslatef(0, 0, -8)

# latitude_circles = [LatitudeCircle(radius, math.pi * (x / (2 * res) + 1)) for x in range(res + 1)] # y
latitude_circles = [LatitudeCircle(radius, 2 * math.pi * (x / (2 * res) + 1 / 2)) for x in range(res + 1)] # z
# longitude_circles = [LongitudeCircle(radius, math.pi * x / res) for x in range(res)] # y
longitude_circles = [LongitudeCircle(radius, math.pi * (x / res + 1)) for x in range(res + 1)] # z

while running:
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			current_key = pygame.key.name(event.key)
			if current_key == "w":
				theta -= d_theta
				theta = max(theta, res // 2)
			elif current_key == "s":
				theta += d_theta
				theta = min(theta, res)
			elif current_key == "a":
				phi += d_phi
			elif current_key == "d":
				phi -= d_phi
			elif current_key == "e":
				glRotatef(1, 1, 0, 0)
			elif current_key == "q":
				glRotatef(1, -1, 0, 0)
			prev_key_states[current_key] = True

		if event.type == pygame.KEYUP:
			prev_key_states[current_key] = False

	if prev_key_states["w"]:
		theta -= d_theta
		theta = max(theta, res // 2)
	if prev_key_states["s"]:
		theta += d_theta
		theta = min(theta, res)
	if prev_key_states["a"]:
		phi += d_phi
	if prev_key_states["d"]:
		phi -= d_phi
	if prev_key_states["e"]:
		glRotatef(1, 1, 0, 0)
	if prev_key_states["q"]:
		glRotatef(1, -1, 0, 0)

	for i in range(res):
		glColor3fv((0, 0, 1))
		latitude_circles[i].show()
		glColor3fv((1, 0, 0))
		longitude_circles[i].show()
	glColor3fv((0, 0, 1))
	latitude_circles[-1].show()
	glColor3fv((1, 0, 0))
	longitude_circles[-1].show()

	pt = (radius * math.sin(math.pi * theta / res) * math.cos(math.pi * phi / res), radius * math.cos(math.pi * theta / res), radius * math.sin(math.pi * theta / res) * math.sin(math.pi * phi / res))

	glLineWidth(2)
	glBegin(GL_LINES)
	glColor3fv((0, 1, 0))
	glVertex3fv((-pt[0], -pt[1], -pt[2]))
	glVertex3fv((0, -radius, 0))
	glEnd()

	glPointSize(10)
	glBegin(GL_POINTS)
	glColor3fv((1, 1, 1))
	glVertex3fv(pt)
	glColor3fv((1, 1, 0))
	projected_pt = (radius * pt[0] / (pt[1] - radius), 0, radius * pt[2] / (pt[1] - radius))
	glVertex3fv(projected_pt)
	glEnd()

	txt_file = open("stereographic_info.txt", 'w')
	txt_file.write(str(radius) + " " + str(projected_pt[0]) + " " + str(projected_pt[2])) # y
	# txt_file.write(str(radius) + " " + str(projected_pt[0]) + " " + str(projected_pt[1])) # z
	txt_file.close()

	pygame.display.flip()
	pygame.time.wait(10)

pygame.quit()
