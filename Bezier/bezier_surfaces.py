from OpenGL.GL import *
from OpenGL.GLU import *
import math, numpy as np, pygame

width = 1600
height = 1200
running = True
u = 0
v = 0
delta_u = 0.01
delta_v = 0.01
prev_key_states = {"w": False, "s": False, "a": False, "d": False}
pmb1s = False
phi = 0
theta = 0
gamma = 0
spd = 0.1

scrn = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

# defining the control points
# ctrl_pts = np.array([[[-1, -1, -1], [0, -1, -1], [1, -1, -1]],
#                      [[-1, -1, 0], [0, 2, 0], [1, -1, 0]],
#                      [[-1, -1, 1], [0, -3, 1], [1, -1, 1]],
#                      [[-1, -1, 1.2], [0, -1, 1.4], [1, -1, 1.7]]], dtype = np.float64)
ctrl_pts = np.array([[[-2, 0, -2], [-2, 0, -1], [-2, 0, 0], [-2, 0, 1], [-2, 0, 2]],
                     [[-1, 0, -2], [-1, -3, -1], [-1, -3, 0], [-1, -3, 1], [-1, 0, 2]],
                     [[0, 0, -2], [0, -3, -1], [0, 15, 0], [0, -3, 1], [0, 0, 2]],
                     [[1, 0, -2], [1, -3, -1], [1, -3, 0], [1, -3, 1], [1, 0, 2]],
                     [[2, 0, -2], [2, 0, -1], [2, 0, 0], [2, 0, 1], [2, 0, 2]]])
n, m = ctrl_pts.shape[:2]
n -= 1
m -= 1

def basisBernsteinPolynomial(n: int, r: int, t: float | int) -> float:
    return binomialCoefficient(n, r) * t ** r * (1 - t) ** (n - r)

def binomialCoefficient(n: int, r: int) -> float:
    return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))

def bbpValues(n: int, t: float | int) -> np.ndarray:
    return np.array([basisBernsteinPolynomial(n, x, t) for x in range(n + 1)])

def pointOnSurface(u: float | int, v: float | int) -> np.ndarray:
    all_u_coeffs = bbpValues(n, u)
    all_v_coeffs = bbpValues(m, v)

    p = np.array([0, 0, 0], dtype = np.float64)
    for i in range(n + 1):
        temp_arr = np.array([0, 0, 0], dtype = np.float64)
        for j in range(m + 1):
            temp_arr += all_v_coeffs[j] * ctrl_pts[i][j]
        p += all_u_coeffs[i] * temp_arr

    return p

# calculating the pts on the surface
all_pts_lst = []
# for i in range(100):
#     temp_lst = []
#     for j in range(100):
#         temp = pointOnSurface(i / 100, j / 100)
#         temp_lst.append(temp)
#     all_pts_lst.append(np.array(temp_lst))
# all_pts_arr = np.array(all_pts_lst)

temp_lst = []
while u < 1:
    while v < 1:
        temp_lst.append(pointOnSurface(u, v))
        v += delta_v
    else:
        all_pts_lst.append(np.array(temp_lst))
        temp_lst = []
        u += delta_u
        v = 0
all_pts_arr = np.array(all_pts_lst)

gluPerspective(45, width / height, 0.1, 50)

glTranslatef(0, 0, -9)

while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            current_key = pygame.key.name(event.key)
            if current_key == "w":
                glTranslatef(0, -spd, 0)
            elif current_key == "s":
                glTranslatef(0, spd, 0)
            elif current_key == "a":
                glTranslatef(spd, 0, 0)
            elif current_key == "d":
                glTranslatef(-spd, 0, 0)
            prev_key_states[current_key] = True

        if event.type == pygame.KEYUP:
            prev_key_states[current_key] = False

    if prev_key_states["w"]:
        glTranslatef(0, -spd, 0)
    if prev_key_states["s"]:
        glTranslatef(0, spd, 0)
    if prev_key_states["a"]:
        glTranslatef(spd, 0, 0)
    if prev_key_states["d"]:
        glTranslatef(-spd, 0, 0)

    if pygame.mouse.get_pressed()[0]:
        if pmb1s:
            current_mouse_pos = pygame.mouse.get_pos()
            horizontal_mouse_move = current_mouse_pos[0] - initial_mouse_pos[0] # ard "y"
            vertical_mouse_move = current_mouse_pos[1] - initial_mouse_pos[1] # ard "x"
            delta_theta = math.cos(phi) * (math.cos(gamma) * vertical_mouse_move + math.sin(gamma) * horizontal_mouse_move)
            delta_phi = math.cos(theta) * (math.sin(gamma) * vertical_mouse_move + math.cos(gamma) * horizontal_mouse_move)
            delta_gamma = math.cos(theta) * math.sin(phi) * vertical_mouse_move + math.cos(phi) * math.sin(theta) * horizontal_mouse_move
            glRotatef(1, delta_theta, delta_phi, delta_gamma)
            theta += delta_theta
            phi += delta_phi
            gamma += delta_gamma
            initial_mouse_pos = current_mouse_pos
        else:
            pmb1s = True
            initial_mouse_pos = pygame.mouse.get_pos()
    else:
        pmb1s = False

    # if u <= 1:
    #     if v <= 1:
    #         temp_lst.append(pointOnSurface(u, v))
    #         v += delta_v
    #     else:
    #         all_pts_lst.append(np.array(temp_lst))
    #         temp_lst = []
    #         v = 0
    #         u += delta_u

    glBegin(GL_LINES)
    glColor3fv((1, 1, 1))
    for i in all_pts_arr:
        for j in i:
            glVertex3fv(j)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3fv((1, 0, 0))
    for i in ctrl_pts:
        for j in i:
            glVertex3fv(j)
    glEnd()

    pygame.display.flip()
    # pygame.time.wait(10)

pygame.quit()
