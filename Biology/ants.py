import pygame, random

pygame.init()

width = 130
height = 130
home = []
food = []
all_ants = []
food_pheromones = []
running = True

scrn = pygame.display.set_mode((width, height))

class Ant:
    def __init__(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.carrying = False
        self.food_pheromone = 0

    def move(self):
        if self.food_pheromone > 0:
            food_pheromones.append([self.pos_x, self.pos_y, 255])
            self.food_pheromone -= 255
##            for m in food_pheromones:
##                if self.pos_x != food_pheromones[m][0] and self.pos_y != food_pheromones[m][1]:
##                    food_pheromones.append([self.pos_x, self.pos_y, 255])
##                    self.food_pheromone -= 255
        self.temp_moves = []
        if not(self.carrying):
            for m in food_pheromones:
                if m[0] == self.pos_x + 1 and m[1] == self.pos_y:
                    for n in range(m[2]):
                        self.temp_moves.append(1)
                if m[0] == self.pos_x - 1 and m[1] == self.pos_y:
                    for n in range(m[2]):
                        self.temp_moves.append(2)
                if m[0] == self.pos_x and m[1] == self.pos_y + 1:
                    for n in range(m[2]):
                        self.temp_moves.append(3)
                if m[0] == self.pos_x and m[1] == self.pos_y - 1:
                    for n in range(m[2]):
                        self.temp_moves.append(4)
        self.temp_moves.append(1)
        self.temp_moves.append(2)
        self.temp_moves.append(3)
        self.temp_moves.append(4)
        self.step = random.choice(self.temp_moves)

        if self.step == 1: self.temp_move = [self.pos_x + 1, self.pos_y]
        elif self.step == 2: self.temp_move = [self.pos_x - 1, self.pos_y]
        elif self.step == 3: self.temp_move = [self.pos_x, self.pos_y + 1]
        else: self.temp_move = [self.pos_x, self.pos_y - 1]

        while self.carrying and self.temp_move in food:
            self.step = random.choice(self.temp_moves)
            if self.step == 1: self.temp_move = [self.pos_x + 1, self.pos_y]
            elif self.step == 2: self.temp_move = [self.pos_x - 1, self.pos_y]
            elif self.step == 3: self.temp_move = [self.pos_x, self.pos_y + 1]
            else: self.temp_move = [self.pos_x, self.pos_y - 1]

        self.pos_x = self.temp_move[0]
        self.pos_y = self.temp_move[1]

##        if self.step == 1: self.pos_x += 1
##        elif self.step == 2: self.pos_x -= 1
##        elif self.step == 3: self.pos_y += 1
##        else: self.pos_y -= 1

    def checkEdges(self):
        if self.pos_x < 0: self.pos_x = 0
        elif self.pos_x >= width: self.pos_x = width - 1
        elif self.pos_y < 0: self.pos_y = 0
        elif self.pos_y >= height: self.pos_y = height - 1

    def atFood(self):
        if not(self.carrying) and [self.pos_x, self.pos_y] in food:
            food.remove([self.pos_x, self.pos_y])
            self.carrying = True
            self.food_pheromone = 25500

    def atHome(self):
        if self.carrying and [self.pos_x, self.pos_y] in home: self.carrying = False

    def show(self):
        if self.carrying: self.clr = (255, 255, 255)
        else: self.clr = (255, 0, 0)
        scrn.set_at((self.pos_x, self.pos_y), self.clr)



for i in range(25):
    for j in range(25):
        home.append([i + 25, j + 25])
        food.append([width - i - 25, height - j - 25])
        food.append([width - i - 50, height - j - 25])
        food.append([width - i - 25, height - j - 50])
        food.append([width - i - 50, height - j - 50])

for i in range(200):
    all_ants.append(Ant(random.choice(home)))

while running:
    scrn.fill((0, 0, 0))

    for i in food_pheromones:
        if i[2] == 0:
            food_pheromones.remove(i)
        else:
            i[2] -= 1
        scrn.set_at((i[0], i[1]), (0, 255, 0))

    for i in home:
        scrn.set_at((i[0], i[1]), (150, 150, 150))

    for i in food:
        scrn.set_at((i[0], i[1]), (200, 200, 0))

    for i in all_ants:
        i.move()
        i.checkEdges()
        i.atFood()
        i.atHome()
        i.show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()

# pheromones: home, food, no food
