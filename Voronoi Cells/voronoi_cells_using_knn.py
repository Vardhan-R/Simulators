# from manim import *
import numpy as np, pygame

pygame.init()

width = 200
height = 200
running = True
# x_1 = 89
x_1 = 20
x_2 = 30
x_3 = 167
y_1 = 25
y_2 = 180
y_3 = 170
# x_4 = 94
# y_4 = 116
x_4 = 130
y_4 = 50

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# pt_A = np.array([x_1, y_1])
# pt_B = np.array([x_2, y_2])
# pt_C = np.array([x_3, y_3])

pts = np.array([[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]])

scrn = pygame.display.set_mode((width, height))
scrn.fill(BLACK)

for i in range(height):
	for j in range(width):
		all_dists = [np.linalg.norm(pts[k] - np.array([j, i])) for k in range(len(pts))]
		min_index = np.argmin(all_dists)
		# if min_index == 3:
		#     scrn.set_at((j, i), BLUE)
		# else:
		#     scrn.set_at((j, i), RED)
		if min_index == 0:
			scrn.set_at((j, i), RED)
		elif min_index == 1:
			scrn.set_at((j, i), GREEN)
		elif min_index == 2:
			scrn.set_at((j, i), BLUE)
		else:
			scrn.set_at((j, i), YELLOW)

	print(i)

for i in pts:
	pygame.draw.circle(scrn, BLACK, tuple(i), 2)


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()

pygame.quit()
