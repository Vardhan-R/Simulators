from built_modules import import_vectors as vect
import math, pygame, random, shelve, time
import matplotlib.pyplot as plt

pygame.init()

for abc in range(10):
    width = 800
    height = 600
    running = True
    black = (0, 0, 0)
    dark_grey = (64, 64, 64)
    grey = (128, 128, 128)
    light_grey = (191, 191, 191)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    dark_green = (0, 128, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    magenta = (255, 0, 255)
    orange = (255, 128, 0)
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
    test_time = 3 # days
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
    # y_lst = [[], [], []] # never infected, never infected + currently infected, never infected + currently infected + removed
    all_vars = [total_nodes, initial_infected, p_interaction, p_transmission, p_asymptomatic, recovery_tm, test_time, vaccinations, vaccination]

    scrn = pygame.display.set_mode((width, height))
    font_size = 12
    font = pygame.font.SysFont("Courier New", font_size)

    class ClickableButton:
        def __init__(self, px, py, w, h, button_clr, text_clr, disp_text):
            self.pos = vect.Vector(px, py)
            self.w = w
            self.h = h
            self.button_clr = button_clr
            self.text = font.render(disp_text, True, text_clr)

        def clicked(self, m_pos):
            if m_pos.x <= self.pos.x <= m_pos.x + self.w and m_pos.y <= self.pos.y <= m_pos.y + self.h:
                return True
            else:
                return False

        def show(self):
            pygame.draw.rect(scrn, self.button_clr, pygame.Rect(self.pos.x - self.w / 2, self.pos.y - self.h / 2, self.w, self.h), 0)
            scrn.blit(self.text, self.text.get_rect(center = (self.pos.x, self.pos.y)))

    class CheckBox:
        def __init__(self, x, y, state):
            self.x = x
            self.y = y
            self.state = state

        def show(self):
            pygame.draw.rect(scrn, light_grey, pygame.Rect(self.x, self.y, 10, 10))
            if self.state:
                pygame.draw.rect(scrn, yellow, pygame.Rect(self.x, self.y, 10, 10), 0)

        def update(self, prev): # prev ==> previous mouse button 1 state
            if not(prev) and pygame.mouse.get_pressed()[0]:
                mx = pygame.mouse.get_pos()[0]
                my = pygame.mouse.get_pos()[1]
                if mx > self.x and mx < self.x + 10 and my > self.y and my < self.y + 10:
                    if self.state:
                        self.state = False
                    else:
                        self.state = True

    class Node:
        def __init__(self, px, py):
            self.pos = vect.Vector(px, py)
            self.clr = white
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
            if self.infected_tm >= recovery_tm and self.clr in (red, yellow):
                self.clr = green
                self.isolated = False
            if self.clr in (red, yellow):
                self.infected_tm += 1
            if self.vaccinated:
                self.isolated = False

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
            all_clrs.append(white)
            temp_var = all_nodes[-1].asymptomatic
            all_asym.append(temp_var)
            all_checkboxes.append([CheckBox(10, 10 * (2 * len(all_nodes) - 1), False), CheckBox(30, 10 * (2 * len(all_nodes) - 1), temp_var)])

        for i in range(n_infections):
            temp_var = random.randrange(0, num)
            while all_nodes[temp_var].clr in (red, yellow):
                temp_var = random.randrange(0, num)
            if all_nodes[temp_var].asymptomatic:
                all_nodes[temp_var].clr = yellow
                all_clrs[temp_var] = yellow
            else:
                all_nodes[temp_var].clr = red
                all_clrs[temp_var] = red
            all_checkboxes[temp_var][0].state = True

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
            p.clr = yellow
        else:
            p.clr = red

    def update():
        for i in all_connections:
            if not(all_nodes[i[0]].isolated or all_nodes[i[1]].isolated):
                if all_nodes[i[0]].clr not in (red, yellow, green, magenta) and all_nodes[i[1]].clr in (red, yellow):
                    if random.randrange(0, 10 ** 5) / 10 ** 5 < p_transmission:
                        if all_nodes[i[0]].asymptomatic:
                            all_nodes[i[0]].clr = yellow
                        else:
                            all_nodes[i[0]].clr = red
                if all_nodes[i[0]].clr in (red, yellow) and all_nodes[i[1]].clr not in (red, yellow, green, magenta):
                    if random.randrange(0, 10 ** 5) / 10 ** 5 < p_transmission:
                        if all_nodes[i[1]].asymptomatic:
                            all_nodes[i[1]].clr = yellow
                        else:
                            all_nodes[i[1]].clr = red

    def vaccinate():
        global total_vaccinations
        for i in range(total_vaccinations, total_vaccinations + vaccinations):
            if i < len(all_nodes):
                all_nodes[i].vaccinated = True
                all_nodes[i].clr = magenta
                all_clrs[i] = magenta
                total_vaccinations += 1

    def end():
        for i in all_nodes:
            if i.clr in (red, yellow):
                return False
        return True

    if load:
        # n = shelve.open("nodes")
        # # imported_lst = n[input(str(len(n)) + ": ")]
        # imported_lst = n["1"]
        # all_nodes = imported_lst[0]
        # all_connections = imported_lst[1]
        # all_clrs = imported_lst[2]
        # all_asym = imported_lst[3]
        # n.close()
        for i in range(len(all_nodes)):
            all_checkboxes.append([CheckBox(10, 10 * (2 * i + 1), all_clrs[i] in (red, yellow)), CheckBox(30, 10 * (2 * i + 1), all_nodes[i].asymptomatic)])

        p = 1
        # print(3)
        # time.sleep(1)
        # print(2)
        # time.sleep(1)
        # print(1)
        # time.sleep(1)
        # print(0)

    if randomise:
        randomNodes(total_nodes, initial_infected)
        randomConnect()

        print(3)
        time.sleep(1)
        print(2)
        time.sleep(1)
        print(1)
        time.sleep(1)
        print(0)

    while running:
        scrn.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            mb = pygame.mouse.get_pressed() # mb ==> mouse button
            if mb[0] and not(pmb1s):
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > 50:
                    all_nodes.append(Node(mouse_pos[0], mouse_pos[1]))
                    all_clrs.append(white)
                    all_asym.append(all_nodes[-1].asymptomatic)
                    all_checkboxes.append([CheckBox(10, 10 * (2 * len(all_nodes) - 1), False), CheckBox(30, 10 * (2 * len(all_nodes) - 1), False)])
                for i in range(len(all_checkboxes)):
                    for j in range(len(all_checkboxes[i])):
                        all_checkboxes[i][j].update(pmb1s)
                pmb1s = True
            if mb[2] and not(pmb2s):
                mouse_pos = pygame.mouse.get_pos()
                entered = False
                for i in range(len(all_nodes)):
                    if((mouse_pos[0] - all_nodes[i].pos.x) ** 2 + (mouse_pos[1] - all_nodes[i].pos.y) ** 2 <= radius ** 2):
                        entered = True
                        if one_selected:
                            connect(selected_node, i)
                            one_selected = False
                        else:
                            selected_node = i
                            one_selected = True
                if not(entered):
                    one_selected = False
                pmb2s = True
            if pmb1s and not(mb[0]):
                pmb1s = False
            if pmb2s and not(mb[2]):
                pmb2s = False

            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "space":
                    p *= -1
                if pygame.key.name(event.key) == "i":
                    all_nodes[-1].clr = red
                    all_clrs[-1] = red
                if pygame.key.name(event.key) == "u":
                    all_nodes[-1].clr = white
                    all_clrs[-1] = white
                # if pygame.key.name(event.key) == "o":
                #     # take out connections
                #     all_nodes.pop(-1)
                #     all_clrs.pop(-1)
                # if pygame.key.name(event.key) == "s":
                #     n = shelve.open("nodes")
                #     temp = []

                #     temp.append(all_nodes.copy())
                #     temp.append(all_connections.copy())
                #     temp.append(all_clrs.copy())
                #     temp.append(all_asym.copy())

                #     # del(n["1"])
                #     # pos = [(388, 310), (398, 187), (530, 209), (401, 90), (559, 90), (241, 230), (170, 101), (131, 201), (160, 333), (520, 337), (672, 343), (729, 235), (255, 398), (433, 447), (293, 490), (390, 508), (511, 479), (671, 484)]
                #     # cons = [(6, 7), (6, 5), (5, 7), (7, 8), (5, 8), (0, 5), (0, 1), (2, 0), (1, 2), (2, 4), (3, 1), (4, 3), (3, 2), (4, 1), (9, 10), (10, 11), (11, 9), (9, 0), (0, 13), (0, 12), (12, 14), (14, 15), (15, 13), (15, 16), (16, 17)]
                #     # all_clrs = [(255, 255, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
                #     # temp_asym = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
                #     # for i in range(len(pos)):
                #     #     all_nodes.append(Node(pos[i][0], pos[i][1]))
                #     #     all_nodes[i].clr = all_clrs[i]
                #     #     all_nodes[i].asymptomatic = temp_asym[i]
                #     # temp.append(all_nodes.copy())
                #     # temp.append(cons.copy())
                #     # temp.append(all_clrs.copy())
                #     # temp.append(temp_asym.copy())

                #     n[str(len(n) + 1)] = temp.copy()
                #     n.close()
                #     print("Saved.")

        pygame.draw.line(scrn, blue, (50, 0), (50, height))

        for i in all_checkboxes:
            for j in i:
                j.show()

        for i in all_connections:
            if not(all_nodes[i[0]].isolated or all_nodes[i[1]].isolated):
                pygame.draw.line(scrn, blue, (all_nodes[i[0]].pos.x, all_nodes[i[0]].pos.y), (all_nodes[i[1]].pos.x, all_nodes[i[1]].pos.y))

        if one_selected:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(scrn, red, (all_nodes[selected_node].pos.x, all_nodes[selected_node].pos.y), (mouse_pos[0], mouse_pos[1]))

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
        # time.sleep(3 - 2 * running)

    all_pos = []
    for i in all_nodes:
        all_pos.append((i.pos.x, i.pos.y))
    # print(all_pos)
    # print(all_connections)
    # print(all_clrs)

    # print(x_lst)
    # print(y_lst)

    plt.axis([0, day + 1, 0, total_nodes + 1])
    plt.plot(x_lst, y_lst[0], 'k-')
    plt.plot(x_lst, y_lst[1], 'r-')
    plt.plot(x_lst, y_lst[2], 'g-')
    if vaccination:
        plt.plot(x_lst, y_lst[3], 'm-')
    plt.xlabel("day")
    plt.ylabel("number of people")
    plt.show()

    # data_file = shelve.open("epidemic_data")
    # temp_lst = [x_lst.copy(), y_lst.copy()]
    # data_file[str(len(data_file) + 1)] = temp_lst.copy()
    # print(len(data_file))
    # data_file.close()

    # vars_file = open("epidemic_vars.txt", 'a')
    # vars_file.write(str(all_vars) + '\n')
    # vars_file.close()
    # print("Saved.")

pygame.quit()
