import math, pygame, time

pygame.init()

width = 600
height = 600
# rows = 10
# cols = 10
k = 0.1
temp_clr = []
clr = []
running = True

for i in range(width): temp_clr.append([0, 0, 0].copy())
for i in range(height): clr.append(temp_clr.copy())
new_clr = clr.copy()

def calc():
    global clr, new_clr
    new_clr[0][0][0] = clr[0][0][0] + math.ceil(k * ((clr[0][1][0] + clr[1][0][0] + clr[1][1][0]) / 3 - clr[0][0][0])) # top-left red
    new_clr[0][0][1] = clr[0][0][1] + math.ceil(k * ((clr[0][1][1] + clr[1][0][1] + clr[1][1][1]) / 3 - clr[0][0][1])) # top-left green
    new_clr[0][0][2] = clr[0][0][2] + math.ceil(k * ((clr[0][1][2] + clr[1][0][2] + clr[1][1][2]) / 3 - clr[0][0][2])) # top-left blue

    new_clr[0][width - 1][0] = clr[0][width - 1][0] + math.ceil(k * ((clr[0][width - 2][0] + clr[1][width - 1][0] + clr[1][width - 2][0]) / 3 - clr[0][width - 1][0])) # top-right red
    new_clr[0][width - 1][1] = clr[0][width - 1][1] + math.ceil(k * ((clr[0][width - 2][1] + clr[1][width - 1][1] + clr[1][width - 2][1]) / 3 - clr[0][width - 1][1])) # top-right green
    new_clr[0][width - 1][2] = clr[0][width - 1][2] + math.ceil(k * ((clr[0][width - 2][2] + clr[1][width - 1][2] + clr[1][width - 2][2]) / 3 - clr[0][width - 1][2])) # top-right blue

    new_clr[height - 1][0][0] = clr[height - 1][0][0] + math.ceil(k * ((clr[height - 1][1][0] + clr[height - 2][0][0] + clr[height - 2][1][0]) / 3 - clr[height - 1][0][0])) # bottom-left red
    new_clr[height - 1][0][1] = clr[height - 1][0][1] + math.ceil(k * ((clr[height - 1][1][1] + clr[height - 2][0][1] + clr[height - 2][1][1]) / 3 - clr[height - 1][0][1])) # bottom-left green
    new_clr[height - 1][0][2] = clr[height - 1][0][2] + math.ceil(k * ((clr[height - 1][1][2] + clr[height - 2][0][2] + clr[height - 2][1][2]) / 3 - clr[height - 1][0][2])) # bottom-left blue

    new_clr[height - 1][width - 1][0] = clr[height - 1][width - 1][0] + math.ceil(k * ((clr[height - 1][width - 2][0] + clr[height - 2][width - 1][0] + clr[height - 2][width - 2][0]) / 3 - clr[height - 1][width - 1][0])) # bottom-right red
    new_clr[height - 1][width - 1][1] = clr[height - 1][width - 1][1] + math.ceil(k * ((clr[height - 1][width - 2][1] + clr[height - 2][width - 1][1] + clr[height - 2][width - 2][1]) / 3 - clr[height - 1][width - 1][1])) # bottom-right green
    new_clr[height - 1][width - 1][2] = clr[height - 1][width - 1][2] + math.ceil(k * ((clr[height - 1][width - 2][2] + clr[height - 2][width - 1][2] + clr[height - 2][width - 2][2]) / 3 - clr[height - 1][width - 1][2])) # bottom-right blue

    # for m in range(1, width - 1): # top
    #     new_clr[0][m][0] = clr[0][m][0] + math.ceil(k * ((clr[0][m - 1][0] + clr[0][m + 1][0] + clr[1][m - 1][0] + clr[1][m][0] + clr[1][m + 1][0]) / 5 - clr[0][m][0])) # red
    #     new_clr[0][m][1] = clr[0][m][1] + math.ceil(k * ((clr[0][m - 1][1] + clr[0][m + 1][1] + clr[1][m - 1][1] + clr[1][m][1] + clr[1][m + 1][1]) / 5 - clr[0][m][1])) # green
    #     new_clr[0][m][2] = clr[0][m][2] + math.ceil(k * ((clr[0][m - 1][2] + clr[0][m + 1][2] + clr[1][m - 1][2] + clr[1][m][2] + clr[1][m + 1][2]) / 5 - clr[0][m][2])) # blue

    clr = new_clr.copy()

scrn = pygame.display.set_mode((width, height))

clr[0][1] = [255, 0, 255]
clr[1][0] = [255, 255, 0]
clr[0][-1] = [255, 0, 0]

while running:
    # scrn.fill((0, 0, 0))
    calc()
    for i in range(height):
        for j in range(width): scrn.set_at((j, i), tuple(clr[i][j]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    pygame.display.update()
    print(clr[0][0])
    time.sleep(1)

pygame.quit()