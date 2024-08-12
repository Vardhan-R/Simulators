from built_modules import import_vectors as vect
from manim import *
import numpy as np, pygame

pygame.init()

width, height = 800, 600
running = True
dt = 1e-3
g = 10
damping = 1e-4
cor = 0.9

class Body:
	def __init__(self, vertices: np.ndarray, edges_k: np.ndarray, edges_l_0: np.ndarray, area: float):
		self.vertices = vertices
		self.n = vertices.size
		self.edges_k = edges_k
		self.edges_l_0 = edges_l_0
		self.area = area

	def calcAcc(self, g: float):
		push_factor = self.n * (np.sqrt(self.area / self.calcArea()) - 1)
		for i in range(self.n - 1):
			for j in range(i + 1, self.n):
				if self.edges_k[i][j] != -1:
					r = self.vertices[j].pos - self.vertices[i].pos
					r_mag = r.mag()
					r_cap = r.normalise()
					f = r_cap * (self.edges_k[i][j] * (self.edges_l_0[i][j] - r_mag))
					self.vertices[i].acc -= f * (1 / self.vertices[i].mass)
					self.vertices[j].acc += f * (1 / self.vertices[j].mass)
					if i == 0:
						self.vertices[j].acc += r_cap * (push_factor / self.vertices[j].mass)
			self.vertices[i].acc.y += g
		self.vertices[-1].acc.y += g

		'''
		PV = P'V'
		FV / A = F'V' / A'
		F' = FVA' / (AV')
		'''

	def calcArea(self) -> float:
		curr_area = 0.0
		for i in range(1, self.n - 1):
			curr_area += abs(self.vertices[0].pos.x * (self.vertices[i].pos.y - self.vertices[i + 1].pos.y)
							+self.vertices[i].pos.x * (self.vertices[i + 1].pos.y - self.vertices[0].pos.y)
							+self.vertices[i + 1].pos.x * (self.vertices[0].pos.y - self.vertices[i].pos.y)) / 2
		return curr_area

	def collision(self, cor: float):
		for vertex in self.vertices:
			vertex.collision(cor)

	def resetAcc(self):
		for vertex in self.vertices:
			vertex.acc = vect.Vector(0, 0)

	def show(self, scrn: pygame.Surface):
		for i in range(self.n - 1):
			for j in range(i + 1, self.n):
				if self.edges_k[i][j] != -1:
					pygame.draw.line(scrn, GREEN, (self.vertices[i].pos.x, self.vertices[i].pos.y), (self.vertices[j].pos.x, self.vertices[j].pos.y))

		for vertex in self.vertices:
			vertex.show(scrn)

	def update(self, dt: float, damping: float):
		for vertex in self.vertices:
			vertex.update(dt, damping)

class Vertex:
	def __init__(self, pos: vect.Vector, vel: vect.Vector, mass: float, radius: float, clr: str | tuple):
		self.pos = pos
		self.vel = vel
		self.acc = vect.Vector(0, 0)
		self.mass = mass
		self.radius = radius
		self.clr = clr

	def collision(self, cor: float):
		if self.pos.y + self.radius >= height:
			self.vel.y *= -cor
			self.pos.y = height - self.radius - 1

	def show(self, scrn: pygame.Surface):
		pygame.draw.circle(scrn, self.clr, (self.pos.x, self.pos.y), self.radius)

	def update(self, dt: float, damping: float):
		self.vel += self.acc * dt
		self.vel *= 1 - damping
		self.pos += self.vel * dt

scrn = pygame.display.set_mode((width, height))

vertices_1 = np.array([Vertex(vect.Vector(300, 100), vect.Vector(0, 0), 100, 5, RED),
					   Vertex(vect.Vector(700, 300), vect.Vector(0, 0), 10, 5, BLUE)])
edges_k_1 = np.array([[-1, 2],
					  [2, -1]])
edges_l_0_1 = np.array([[-1, 300],
						[300, -1]])

vertices_2 = np.array([Vertex(vect.Vector(300, 100), vect.Vector(0, 0), 7, 5, RED),
					   Vertex(vect.Vector(700, 300), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(500, 500), vect.Vector(0, 0), 9, 5, RED)])
edges_k_2 = np.array([[-1, 2, 3],
					  [2, -1, 4],
					  [3, 4, -1]])
edges_l_0_2 = np.array([[-1, 90, 200],
						[90, -1, 400],
						[200, 400, -1]])

vertices_2 = np.array([Vertex(vect.Vector(400, 300), vect.Vector(0, 0), 7, 5, RED),
					   Vertex(vect.Vector(700, 300), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(200, 500), vect.Vector(0, 0), 9, 5, RED),
					   Vertex(vect.Vector(300, 100), vect.Vector(0, 0), 9, 5, RED)])
edges_k_2 = np.array([[-1, 2, 2, 2],
					  [2, -1, 2, 2],
					  [2, 2, -1, 2],
					  [2, 2, 2, -1]])
edges_l_0_2 = np.array([[-1, 200, 200, 200],
						[200, -1, 400, 400],
						[200, 400, -1, 400],
						[200, 400, 400, -1]])

vertices_3 = np.array([Vertex(vect.Vector(400, 300), vect.Vector(0, 0), 9, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 0 / 10), 300 + 100 * np.sin(2 * np.pi * 0 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 1 / 10), 300 + 100 * np.sin(2 * np.pi * 1 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 2 / 10), 300 + 100 * np.sin(2 * np.pi * 2 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 3 / 10), 300 + 100 * np.sin(2 * np.pi * 3 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 4 / 10), 300 + 100 * np.sin(2 * np.pi * 4 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 5 / 10), 300 + 100 * np.sin(2 * np.pi * 5 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 6 / 10), 300 + 100 * np.sin(2 * np.pi * 6 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 7 / 10), 300 + 100 * np.sin(2 * np.pi * 7 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 8 / 10), 300 + 100 * np.sin(2 * np.pi * 8 / 10)), vect.Vector(0, 0), 8, 5, RED),
					   Vertex(vect.Vector(400 + 100 * np.cos(2 * np.pi * 9 / 10), 300 + 100 * np.sin(2 * np.pi * 9 / 10)), vect.Vector(0, 0), 8, 5, RED)])
edges_k_3 = np.array([[-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
					  [-1, -1, 2, -1, -1, -1, -1, -1, -1, -1, 2],
					  [-1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
edges_l_0_3 = np.array([[-1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
					  [-1, -1, 50, -1, -1, -1, -1, -1, -1, -1, 50],
					  [-1, -1, -1, 50, -1, -1, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, 50, -1, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, 50, -1, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, 50, -1, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, 50, -1, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, 50, -1, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, 50, -1],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 50],
					  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])

body_1 = Body(vertices_1, edges_k_1, edges_l_0_1, 1e5)
body_2 = Body(vertices_2, edges_k_2, edges_l_0_2, 1e5)
body_3 = Body(vertices_3, edges_k_3, edges_l_0_3, 5e7)

while running:
	scrn.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	body_3.resetAcc()
	body_3.calcAcc(g)
	body_3.update(dt, damping)
	body_3.collision(cor)
	body_3.show(scrn)

	pygame.display.update()