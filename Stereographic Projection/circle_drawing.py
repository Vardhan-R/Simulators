from manim import *
import math, pygame

pygame.init()

width = 600
height = 600
running = True
half_width = width / 2
half_height = height / 2
res = 32

scrn = pygame.display.set_mode((width, height))

# latitude_circles.append([(radius * math.sin(math.pi * a / res) * math.cos(2 * math.pi * b / res) / (math.sin(math.pi * a / res) * math.sin(2 * math.pi * b / res) - 1) + half_width, radius * math.cos(math.pi * a / res) / (math.sin(math.pi * a / res) * math.sin(2 * math.pi * b / res) - 1) + half_height) for b in range(res // 2, res + 1)])
latitude_circles = [[((half_width - 50) * math.sin(math.pi * a / res) * math.cos(2 * math.pi * b / res) / (math.sin(math.pi * a / res) * math.sin(2 * math.pi * b / res) - 1) + half_width, (half_width - 50) * math.cos(math.pi * a / res) / (math.sin(math.pi * a / res) * math.sin(2 * math.pi * b / res) - 1) + half_height) for b in range(res // 2, res + 1)] for a in range(res)]
longitude_circles = []
for a in range(res // 2, res + 1):
	if a == 3 * res // 4:
		longitude_circles.append([(half_width, half_height - (half_width - 50)), (half_width, half_height + (half_width - 50))])
	else:
		longitude_circles.append([((half_width - 50) * math.sin(2 * math.pi * b / res) * math.cos(2 * math.pi * a / res) / (math.sin(2 * math.pi * b / res) * math.sin(2 * math.pi * a / res) - 1) + half_width, (half_width - 50) * math.cos(2 * math.pi * b / res) / (math.sin(2 * math.pi * b / res) * math.sin(2 * math.pi * a / res) - 1) + half_height) for b in range(res)])

def show():
	for i in range(len(latitude_circles)):
		for j in range(len(latitude_circles[i]) - 1):
			pygame.draw.line(scrn, BLUE, latitude_circles[i][j], latitude_circles[i][j + 1])
			try:
				pygame.draw.line(scrn, RED, longitude_circles[i][j], longitude_circles[i][j + 1])
			except:
				pass

while running:
	scrn.fill(WHITE)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


	txt_file = open("stereographic_info.txt", 'r')
	temp_lst = txt_file.readline().split(" ")
	txt_file.close()
	try:
		radius = float(temp_lst[0])
		pt = (float(temp_lst[1]), float(temp_lst[2]))
	except:
		pass

	temp = (half_width - 50) / radius
	pygame.draw.circle(scrn, RED, (half_width, half_height), half_width - 50, 1)

	# for i in range(res):
	#     pygame.draw.circle(scrn, BLUE, (half_width, half_height), (half_width - 50) * math.sin(math.pi * i / (2 * res)) / (1 + math.cos(math.pi * i / (2 * res))), 1)
	#     for j in range(2):
	#         pygame.draw.line(scrn, RED, (half_width, half_height), (half_width + (half_width - 50) * math.cos((2 * i + j) * math.pi / res), half_height + (half_width - 50) * math.sin((2 * i + j) * math.pi / res)))

	show()

	pygame.draw.circle(scrn, BLACK, (temp * pt[0] + half_width, temp * pt[1] + half_height), 5)

	pygame.display.update()
	pygame.time.wait(100)

pygame.quit()
