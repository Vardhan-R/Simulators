import math, pygame, random, time

pygame.init()

width = 600
height = 600
rows = 12
cols = 12
row_size = int(height / rows)
col_size = int(width / cols)
k = 0.001
clr = []
new_clr = []
running = True

for i in range(rows):
    clr.append([])
    new_clr.append([])
    for j in range(cols):
        clr[i].append([])
        new_clr[i].append([])
        # clr[i][j] = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
        # new_clr[i][j] = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
        clr[i][j] = [0, 0, 0]
        new_clr[i][j] = [0, 0, 0]

def roundOff(x):
    if x < 0: return math.floor(x)
    else: return math.ceil(x)

def calcAve(l): # l = [[row, col], [row, col], [row, col], ..., [row, col]]
    temp_clr_r = 0
    for m in l:
        temp_clr_r += clr[m[0]][m[1]][0]

def calcClr():
    global clr, new_clr
    new_clr[0][0][0] = clr[0][0][0] + roundOff(k * ((clr[0][1][0] + clr[1][0][0] + clr[1][1][0]) / 3 - clr[0][0][0])) # top-left red
    new_clr[0][0][1] = clr[0][0][1] + roundOff(k * ((clr[0][1][1] + clr[1][0][1] + clr[1][1][1]) / 3 - clr[0][0][1])) # top-left green
    new_clr[0][0][2] = clr[0][0][2] + roundOff(k * ((clr[0][1][2] + clr[1][0][2] + clr[1][1][2]) / 3 - clr[0][0][2])) # top-left blue

    new_clr[0][cols - 1][0] = clr[0][cols - 1][0] + roundOff(k * ((clr[0][cols - 2][0] + clr[1][cols - 1][0] + clr[1][cols - 2][0]) / 3 - clr[0][cols - 1][0])) # top-right red
    new_clr[0][cols - 1][1] = clr[0][cols - 1][1] + roundOff(k * ((clr[0][cols - 2][1] + clr[1][cols - 1][1] + clr[1][cols - 2][1]) / 3 - clr[0][cols - 1][1])) # top-right green
    new_clr[0][cols - 1][2] = clr[0][cols - 1][2] + roundOff(k * ((clr[0][cols - 2][2] + clr[1][cols - 1][2] + clr[1][cols - 2][2]) / 3 - clr[0][cols - 1][2])) # top-right blue

    new_clr[rows - 1][0][0] = clr[rows - 1][0][0] + roundOff(k * ((clr[rows - 1][1][0] + clr[rows - 2][0][0] + clr[rows - 2][1][0]) / 3 - clr[rows - 1][0][0])) # bottom-left red
    new_clr[rows - 1][0][1] = clr[rows - 1][0][1] + roundOff(k * ((clr[rows - 1][1][1] + clr[rows - 2][0][1] + clr[rows - 2][1][1]) / 3 - clr[rows - 1][0][1])) # bottom-left green
    new_clr[rows - 1][0][2] = clr[rows - 1][0][2] + roundOff(k * ((clr[rows - 1][1][2] + clr[rows - 2][0][2] + clr[rows - 2][1][2]) / 3 - clr[rows - 1][0][2])) # bottom-left blue

    new_clr[rows - 1][cols - 1][0] = clr[rows - 1][cols - 1][0] + roundOff(k * ((clr[rows - 1][cols - 2][0] + clr[rows - 2][cols - 1][0] + clr[rows - 2][cols - 2][0]) / 3 - clr[rows - 1][cols - 1][0])) # bottom-right red
    new_clr[rows - 1][cols - 1][1] = clr[rows - 1][cols - 1][1] + roundOff(k * ((clr[rows - 1][cols - 2][1] + clr[rows - 2][cols - 1][1] + clr[rows - 2][cols - 2][1]) / 3 - clr[rows - 1][cols - 1][1])) # bottom-right green
    new_clr[rows - 1][cols - 1][2] = clr[rows - 1][cols - 1][2] + roundOff(k * ((clr[rows - 1][cols - 2][2] + clr[rows - 2][cols - 1][2] + clr[rows - 2][cols - 2][2]) / 3 - clr[rows - 1][cols - 1][2])) # bottom-right blue

    for m in range(1, cols - 1): # top and bottom
        new_clr[0][m][0] = clr[0][m][0] + roundOff(k * ((clr[0][m - 1][0] + clr[0][m + 1][0] + clr[1][m - 1][0] + clr[1][m][0] + clr[1][m + 1][0]) / 5 - clr[0][m][0])) # red
        new_clr[0][m][1] = clr[0][m][1] + roundOff(k * ((clr[0][m - 1][1] + clr[0][m + 1][1] + clr[1][m - 1][1] + clr[1][m][1] + clr[1][m + 1][1]) / 5 - clr[0][m][1])) # green
        new_clr[0][m][2] = clr[0][m][2] + roundOff(k * ((clr[0][m - 1][2] + clr[0][m + 1][2] + clr[1][m - 1][2] + clr[1][m][2] + clr[1][m + 1][2]) / 5 - clr[0][m][2])) # blue

        new_clr[rows - 1][m][0] = clr[rows - 1][m][0] + roundOff(k * ((clr[rows - 2][m - 1][0] + clr[rows - 2][m][0] + clr[rows - 2][m + 1][0] + clr[rows - 1][m - 1][0] + clr[rows - 1][m + 1][0]) / 5 - clr[rows - 1][m][0])) # red
        new_clr[rows - 1][m][1] = clr[rows - 1][m][1] + roundOff(k * ((clr[rows - 2][m - 1][1] + clr[rows - 2][m][1] + clr[rows - 2][m + 1][1] + clr[rows - 1][m - 1][1] + clr[rows - 1][m + 1][1]) / 5 - clr[rows - 1][m][1])) # green
        new_clr[rows - 1][m][2] = clr[rows - 1][m][2] + roundOff(k * ((clr[rows - 2][m - 1][2] + clr[rows - 2][m][2] + clr[rows - 2][m + 1][2] + clr[rows - 1][m - 1][2] + clr[rows - 1][m + 1][2]) / 5 - clr[rows - 1][m][2])) # blue

    for m in range(1, rows - 1): # left and right
        new_clr[m][0][0] = clr[m][0][0] + roundOff(k * ((clr[m - 1][0][0] + clr[m - 1][1][0] + clr[m][1][0] + clr[m + 1][0][0] + clr[m + 1][1][0]) / 5 - clr[m][0][0])) # red
        new_clr[m][0][1] = clr[m][0][1] + roundOff(k * ((clr[m - 1][0][1] + clr[m - 1][1][1] + clr[m][1][1] + clr[m + 1][0][1] + clr[m + 1][1][1]) / 5 - clr[m][0][1])) # green
        new_clr[m][0][2] = clr[m][0][2] + roundOff(k * ((clr[m - 1][0][2] + clr[m - 1][1][2] + clr[m][1][2] + clr[m + 1][0][2] + clr[m + 1][1][2]) / 5 - clr[m][0][2])) # blue

        new_clr[m][cols - 1][0] = clr[m][cols - 1][0] + roundOff(k * ((clr[m - 1][cols - 2][0] + clr[m - 1][cols - 1][0] + clr[m][cols - 2][0] + clr[m + 1][cols - 2][0] + clr[m + 1][cols - 1][0]) / 5 - clr[m][cols - 1][0])) # red
        new_clr[m][cols - 1][1] = clr[m][cols - 1][1] + roundOff(k * ((clr[m - 1][cols - 2][1] + clr[m - 1][cols - 1][1] + clr[m][cols - 2][1] + clr[m + 1][cols - 2][1] + clr[m + 1][cols - 1][1]) / 5 - clr[m][cols - 1][1])) # green
        new_clr[m][cols - 1][2] = clr[m][cols - 1][2] + roundOff(k * ((clr[m - 1][cols - 2][2] + clr[m - 1][cols - 1][2] + clr[m][cols - 2][2] + clr[m + 1][cols - 2][2] + clr[m + 1][cols - 1][2]) / 5 - clr[m][cols - 1][2])) # blue

    for m in range(1, rows - 1): # centre
        for n in range(1, cols - 1):
            new_clr[m][n][0] = clr[m][n][0] + roundOff(k * ((clr[m - 1][n - 1][0] + clr[m - 1][n][0] + clr[m - 1][n + 1][0] + clr[m][n - 1][0] + clr[m][n + 1][0] + clr[m + 1][n - 1][0] + clr[m + 1][n][0] + clr[m + 1][n + 1][0]) / 8 - clr[m][n][0])) # red
            new_clr[m][n][1] = clr[m][n][1] + roundOff(k * ((clr[m - 1][n - 1][1] + clr[m - 1][n][1] + clr[m - 1][n + 1][1] + clr[m][n - 1][1] + clr[m][n + 1][1] + clr[m + 1][n - 1][1] + clr[m + 1][n][1] + clr[m + 1][n + 1][1]) / 8 - clr[m][n][1])) # green
            new_clr[m][n][2] = clr[m][n][2] + roundOff(k * ((clr[m - 1][n - 1][2] + clr[m - 1][n][2] + clr[m - 1][n + 1][2] + clr[m][n - 1][2] + clr[m][n + 1][2] + clr[m + 1][n - 1][2] + clr[m + 1][n][2] + clr[m + 1][n + 1][2]) / 8 - clr[m][n][2])) # blue

    for m in range(len(new_clr)):
        for n in range(len(new_clr[m])): clr[m][n] = new_clr[m][n].copy()

scrn = pygame.display.set_mode((width, height))

# clr[math.floor(rows / 2)][math.floor(cols / 2)] = [255, 255, 255]
# clr[math.floor(rows / 2)][math.floor(cols / 2) + 1] = [255, 255, 255]
# clr[math.floor(rows / 2) + 1][math.floor(cols / 2)] = [255, 255, 255]
# clr[math.floor(rows / 2) + 1][math.floor(cols / 2) + 1] = [255, 255, 255]

for i in range(int(5)):
    for j in range(rows):
        clr[j][i] = [255, 0, 0]
        clr[j][cols - i - 1] = [0, 0, 255]

while running:
    calcClr()
    for i in range(rows):
        for j in range(cols): pygame.draw.rect(scrn, tuple(clr[i][j]), pygame.Rect(j * col_size, i * row_size, col_size, row_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    pygame.display.update()
    time.sleep(0.1)

pygame.quit()