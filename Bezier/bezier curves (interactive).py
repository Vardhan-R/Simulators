import math, pygame, random, time

pygame.init()

width = 600
height = 600
rows = 60
cols = 60
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
violet = (255, 0, 255)
orange = (255, 128, 0)
clrs = [green, yellow, violet, orange, dark_grey, light_grey, white]
# font_size = 12
# font = pygame.font.Font("freesansbold.ttf", font_size)

class Vector:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

pts = [Vector(100, 200), Vector(300, 250), Vector(350, 400), Vector(450, 150), Vector(500, 350), Vector(250, 410)]
# pts = [Vector(100, 200), Vector(200, 300), Vector(300, 200)]
final_pts = []
r = 0
c = 1000
disp_all_lines = 1
done = -1
pause = -1
show_final_only = -1
show_grid = -1
snap_to_grid = -1

def add(v1, v2): return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sub(v1, v2): return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def mult(k, v): return Vector(k * v.x, k * v.y, k * v.z)

def div(k, v): return Vector(v.x / k, v.y / k, v.z / k)

def dot(v1, v2): return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def cross(v1, v2): return Vector(det([[v1.y, v1.z], [v2.y, v2.z]]), det([[v1.x, v1.z], [v2.x, v2.z]]), det([[v1.x, v1.y], [v2.x, v2.y]]))

def det(t):
    if len(t) > 2:
        s = 0
        for m in range(len(t)):
            p = []
            for n in t:
                p.append(n.copy())
            p.pop(0)
            for n in range(len(p)):
                p[n].pop(m)
            s += (-1) ** m * t[0][m] * det(p)
        return s
    elif len(t) == 2: return t[0][0] * t[1][1] - t[0][1] * t[1][0]
    elif len(t) == 1: return t[0][0]
    else: return 0

def cuttingPt(pt1, pt2, r): return Vector(r * pt2.x + (1 - r) * pt1.x, r * pt2.y + (1 - r) * pt1.y)

def connect(surface, clr, pts, close = False):
    for m in range(len(pts) - 1): pygame.draw.line(surface, clr, (pts[m].x, pts[m].y), (pts[m + 1].x, pts[m + 1].y))
    if close: pygame.draw.line(surface, clr, (pts[-1].x, pts[-1].y), (pts[0].x, pts[0].y))

def reset():
    global disp_all_lines, done, r
    disp_all_lines = 1
    done = -1
    r = 0
    all_pts.clear()
    final_pts.clear()

def movePt(click, mouse_x, mouse_y):
    global r
    pygame.draw.circle(scrn, red, (pts[0].x, pts[0].y), 10)
    for m in pts[1: -1]: pygame.draw.circle(scrn, dark_green, (m.x, m.y), 10)
    pygame.draw.circle(scrn, grey, (pts[-1].x, pts[-1].y), 10)
    if click:
        for m in range(len(pts)):
            if (pts[m].x - mouse_x) ** 2 + (pts[m].y - mouse_y) ** 2 < 100:
                if snap_to_grid == 1: pts[m] = Vector(round(cols * mouse_x / width) * width / cols, round( rows * mouse_y / height) * height / rows)
                else: pts[m] = Vector(mouse_x, mouse_y)
                reset()

def grid(surface, rows, cols):
    for m in range(rows): pygame.draw.line(surface, dark_grey, (0, m * height / rows), (width, m * height / rows))
    for m in range(cols): pygame.draw.line(surface, dark_grey, (m * width / cols, 0), (m * width / cols, height))

# def button(name, var, pos_x, pos_y, w, h, m, mouse_x, mouse_y):
#     if var == 1: clr = dark_grey
#     else: clr = light_grey

#     pygame.draw.rect(scrn, clr, pygame.Rect(pos_x, pos_y, w, h))
#     text = font.render(str(name), True, black)
#     text_rect = text.get_rect(center = (pos_x + w / 2, pos_y + h / 2))
#     scrn.blit(text, text_rect)

#     if m:
#         if (pos_x <= mouse_x <= pos_x + w and pos_y <= mouse_y <= pos_y + h): return -var
#     else: return var

scrn = pygame.display.set_mode((width, height))

instructions = ["Pause/Play [space]", "Display all lines [a]", "Show final only [s]", "Reset [r]", "Remove last control point [o]", "Add control point [p]", "Show grid [g]", "Snap to grid [h]"]
for i in instructions: print(i)

while running:
    scrn.fill(black)
    if show_grid == 1: grid(scrn, rows, cols)
    connect(scrn, blue, pts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "space": pause *= -1

            if pygame.key.name(event.key) == "a": disp_all_lines *= -1

            if pygame.key.name(event.key) == "s":
                show_final_only *= -1
                final_pts.clear()

            if pygame.key.name(event.key) == "r": reset()

            if pygame.key.name(event.key) == "g":
                show_grid *= -1
                snap_to_grid = -1

            if pygame.key.name(event.key) == "h":
                if show_grid == 1: snap_to_grid *= -1

            if pause == 1:
                if pygame.key.name(event.key) == "o":
                    if len(pts) > 2:
                        pts.pop()
                        reset()

                if pygame.key.name(event.key) == "p":
                    pts.append(Vector(width / 2, height / 2))
                    reset()

    # disp_all_lines = button("Show all lines [a]", disp_all_lines, 5, 5, 100, 25, pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    if done == -1 and pause == -1 and show_final_only == -1:
        all_pts = []
        temp_pts = []
        for i in range(len(pts) - 1): temp_pts.append(cuttingPt(pts[i], pts[i + 1], r / c))
        while len(temp_pts) != 1:
            all_pts.append(temp_pts.copy())
            for i in range(len(temp_pts) - 1): temp_pts[i] = cuttingPt(temp_pts[i], temp_pts[i + 1], r / c)
            temp_pts.pop()

        all_pts.reverse()
        final_pts.append(temp_pts[0])

    elif show_final_only == 1:
        reset()
        for i in range(c + 1):
            temp_pts = []
            for j in range(len(pts) - 1): temp_pts.append(cuttingPt(pts[j], pts[j + 1], i / c))
            while len(temp_pts) != 1:
                for j in range(len(temp_pts) - 1): temp_pts[j] = cuttingPt(temp_pts[j], temp_pts[j + 1], i / c)
                temp_pts.pop()

            final_pts.append(temp_pts[0])

    if disp_all_lines == 1:
        if not(pygame.mouse.get_pressed()[0] and pause == 1):
            for i in range(len(all_pts)): connect(scrn, clrs[i], all_pts[i])
    connect(scrn, red, final_pts)

    if pause == 1: movePt(pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pygame.display.update()
    time.sleep(0.01)

    if r == c:
        disp_all_lines = -1
        done = 1
        r = 0

    if done == -1 and pause == -1: r += 1

pygame.quit()

# movable pts (done)
# add or remove pts (done)
# show final curve (done)
# run (done)
# animate (done)
# pause and play (done)
# clickable buttons (on-scrn)