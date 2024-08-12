from built_modules import import_vectors as vect
from manim import *
import numpy as np, pygame

pygame.init()

width = 800
height = 600
running = True
g = 1
ang_disp = np.pi / 4
ang_vel = 0
ang_acc = 0
pos = width / 2
acc = 0
vel = 0
l = 200
dt = 0.1

scrn = pygame.display.set_mode((width, height))

while running:
	scrn.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	m_x = pygame.mouse.get_pos()[0]
	acc = 3 * (2 * m_x / width - 1)
	vel += acc * dt * 10 ** (-1) / 5
	pos += vel * dt * 10 ** (-1) / 5
	ang_acc = (-acc * np.cos(ang_disp) + g * np.sin(ang_disp)) / l
	ang_vel += ang_acc * dt
	ang_disp += ang_acc * dt

	if abs(ang_disp) >= np.pi / 2:
		print("Failed!")
		pos = width / 2
		vel = 0
		ang_disp = np.pi / 4
		ang_vel = 0

	pygame.draw.rect(scrn, WHITE, pygame.Rect(pos - 50, 3 * height / 4, 100, 10))
	pygame.draw.line(scrn, WHITE, (pos, 3 * height / 4), (pos + l * np.sin(ang_disp), 3 * height / 4 - l * np.cos(ang_disp)))
	pygame.draw.circle(scrn, WHITE, (pos + l * np.sin(ang_disp), 3 * height / 4 - l * np.cos(ang_disp)), 5)

	pygame.display.update()

pygame.quit()