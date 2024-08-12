from built_modules import import_vectors as vect
from manim import *
import math, matplotlib.pyplot as plt, pygame, random, shelve, time

pygame.init()

width = 800
height = 600
running = True
radius = 5
pos_per_num = 3
total_vaccinations = 0
p = -1
day = 0
total_nodes = 500 # only if randomising
initial_infected = 4 # only if randomising
p_interaction = 6 / total_nodes
p_transmission = 0.05
p_asymptomatic = 0.1
recovery_tm = 14 # days
test_time = 1 # days
vaccinations = 10 # per day
vaccination = False
load = False
randomise = True
one_selected = False
pmb1s = False
pmb2s = False
all_nodes = []
all_connections = []
all_clrs = []
all_asym = []
all_checkboxes = []
x_lst = []
y_lst = [[], [], [], []] # never infected and not vaccinated, currently infected, removed and not vaccinated, vaccinated

class Node:
    def __init__(self, px, py):
        self.pos = vect.Vector(px, py)
        self.clr = WHITE
        self.infected_tm = 0
        self.isolated = False
        self.vaccinated = False
        if random.randrange(0, 10 ** 5) / 10 ** 5 < p_asymptomatic:
            self.asymptomatic = True
        else:
            self.asymptomatic = False

    def show(self):
        pygame.draw.circle(scrn, self.clr, (self.pos.x, self.pos.y), radius)

    def update(self):
        if not(self.asymptomatic) and self.infected_tm >= test_time:
            self.isolated = True
        if self.infected_tm >= recovery_tm and self.clr in (RED, YELLOW):
            self.clr = GREEN
            self.isolated = False
        if self.clr in (RED, YELLOW):
            self.infected_tm += 1
        if self.vaccinated:
            self.isolated = False

scrn = pygame.display.set_mode((width, height))

def connect(p_1, p_2):
    if p_1 != p_2 and (p_1, p_2) not in all_connections and (p_2, p_1) not in all_connections:
        all_connections.append((p_1, p_2))
    else:
        try:
            all_connections.remove((p_1, p_2))
        except:
            pass
        try:
            all_connections.remove((p_2, p_1))
        except:
            pass

def randomNodes(num, n_infections):
    for i in range(num):
        all_nodes.append(Node(random.randrange(60, width - 10), random.randrange(10, height - 10)))
        all_clrs.append(WHITE)
        temp_var = all_nodes[-1].asymptomatic
        all_asym.append(temp_var)
        # all_checkboxes.append([CheckBox(10, 10 * (2 * len(all_nodes) - 1), False), CheckBox(30, 10 * (2 * len(all_nodes) - 1), temp_var)])

    for i in range(n_infections):
        temp_var = random.randrange(0, num)
        while all_nodes[temp_var].clr in (RED, YELLOW):
            temp_var = random.randrange(0, num)
        if all_nodes[temp_var].asymptomatic:
            all_nodes[temp_var].clr = YELLOW
            all_clrs[temp_var] = YELLOW
        else:
            all_nodes[temp_var].clr = RED
            all_clrs[temp_var] = RED
        # all_checkboxes[temp_var][0].state = True

def randomConnect():
    global all_connections
    all_connections.clear()
    for i in range(len(all_nodes)):
        if not(all_nodes[i].isolated):
            for j in range(i, len(all_nodes)):
                if i != j:
                    if not(all_nodes[j].isolated):
                        if random.randrange(0, 10 ** 5) / 10 ** 5 < p_interaction:
                                all_connections.append((i, j))

def infect(p):
    if p.asymptomatic:
        p.clr = YELLOW
    else:
        p.clr = RED

def update():
    for i in all_connections:
        if not(all_nodes[i[0]].isolated or all_nodes[i[1]].isolated):
            if all_nodes[i[0]].clr not in (RED, YELLOW, GREEN, MAGENTA) and all_nodes[i[1]].clr in (RED, YELLOW):
                if random.randrange(0, 10 ** 5) / 10 ** 5 < p_transmission:
                    if all_nodes[i[0]].asymptomatic:
                        all_nodes[i[0]].clr = YELLOW
                    else:
                        all_nodes[i[0]].clr = RED
            if all_nodes[i[0]].clr in (RED, YELLOW) and all_nodes[i[1]].clr not in (RED, YELLOW, GREEN, MAGENTA):
                if random.randrange(0, 10 ** 5) / 10 ** 5 < p_transmission:
                    if all_nodes[i[1]].asymptomatic:
                        all_nodes[i[1]].clr = YELLOW
                    else:
                        all_nodes[i[1]].clr = RED

def vaccinate():
    global total_vaccinations
    for i in range(total_vaccinations, total_vaccinations + vaccinations):
        if i < len(all_nodes):
            all_nodes[i].vaccinated = True
            all_nodes[i].clr = MAGENTA
            all_clrs[i] = MAGENTA
            total_vaccinations += 1

def end():
    for i in all_nodes:
        if i.clr in (RED, YELLOW):
            return False
    return True

randomNodes(total_nodes, initial_infected)
randomConnect()

while running:
    scrn.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.draw.line(scrn, BLUE, (50, 0), (50, height))

    # for i in all_checkboxes:
    #     for j in i:
    #         j.show()

    for i in all_connections:
        if not(all_nodes[i[0]].isolated or all_nodes[i[1]].isolated):
            pygame.draw.line(scrn, BLUE, (all_nodes[i[0]].pos.x, all_nodes[i[0]].pos.y), (all_nodes[i[1]].pos.x, all_nodes[i[1]].pos.y))

    # if one_selected:
    #     mouse_pos = pygame.mouse.get_pos()
    #     pygame.draw.line(scrn, RED, (all_nodes[selected_node].pos.x, all_nodes[selected_node].pos.y), (mouse_pos[0], mouse_pos[1]))

    for i in all_nodes:
        i.show()

    if p == 1:
        temp_lst = [0, 0, 0, 0]
        for i in all_nodes:
            if i.clr == white:
                temp_lst[0] += 1
                # temp_lst[1] += 1
                # temp_lst[2] += 1
            elif i.clr in (red, yellow):
                temp_lst[1] += 1
                # temp_lst[2] += 1
            elif i.clr == green:
                temp_lst[2] += 1
            else:
                temp_lst[3] += 1
        x_lst.append(day)
        y_lst[0].append(temp_lst[0])
        y_lst[1].append(temp_lst[1])
        y_lst[2].append(temp_lst[2])
        y_lst[3].append(temp_lst[3])

        if not(end()):
            for i in all_nodes:
                i.update()
            update()
            if vaccination:
                vaccinate()
            print("Day", day)
            day += 1
            if randomise:
                randomConnect()
        else:
            running = False
            # time.sleep(3)

        # time.sleep(0.1)
    else:
        for i in range(len(all_checkboxes)):
            if all_checkboxes[i][0].state:
                if all_checkboxes[i][1].state:
                    all_nodes[i].clr = yellow
                    all_clrs[i] = yellow
                else:
                    all_nodes[i].clr = red
                    all_clrs[i] = red
            else:
                all_nodes[i].clr = white
                all_clrs[i] = white
            if all_checkboxes[i][1].state:
                all_nodes[i].asymptomatic = True
            else:
                all_nodes[i].asymptomatic = False

            text = font.render(str(i + 1), True, blue)
            scrn.blit(text, (all_nodes[i].pos.x, all_nodes[i].pos.y))
            scrn.blit(text, (1, 10 * (2 * i + 1)))

    pygame.display.update()

all_pos = []
for i in all_nodes:
    all_pos.append((i.pos.x, i.pos.y))