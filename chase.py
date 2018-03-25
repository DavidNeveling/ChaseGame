import pygame, sys, math, random
from pygame.locals import *

width = 400
height = 300

class circ:
    def __init__(self, color, x, y, rad, dir, speed):
        self.color = color
        self.x = x
        self.y = y
        self.radius = rad
        self.dir = dir
        self.speed = speed

def loadCircles(num_obstacles):
    list = []
    for i in range(num_obstacles):
        temp_dir = ""
        if random.randrange(2) > 0:
            temp_dir = "left"
        else:
            temp_dir = "right"
        temp = circ(pygame.Color(255, 0, 255), random.randrange(width), random.randrange(height), 5, temp_dir, .1)
        while temp.x < 100 and temp.y < 100:
            temp = circ(pygame.Color(255, 0, 255), random.randrange(width), random.randrange(height), 5, temp_dir, .1)
        list.append(temp)
    return list

def drawCircles(surf, list, update):
    for circ in list:
        pygame.draw.circle(surf, circ.color, (int(circ.x), int(circ.y)), circ.radius, 0)
        if update:

            if circ.x < 0:
                circ.dir = "right"
            if circ.x > width:
                circ.dir = "left"

            if circ.dir == "right":
                circ.x += circ.speed
            if circ.dir == "left":
                circ.x -= circ.speed

def reset():
    global circles
    global num_obstacles
    circles = loadCircles(num_obstacles)

    global p_x
    p_x = 0
    global p_y
    p_y = 0
    global p_radius
    p_radius = 10

    global e_x
    e_x = width
    global e_y
    e_y = height
    global e_radius
    e_radius = 10

    global p_speed
    p_speed = .5
    global e_speed
    e_speed = .2

    global left
    left = False
    global right
    right = False
    global up
    up = False
    global down
    down = False
    global dip
    dip = True
    global slope
    slope = 0

    global GAMEOVER
    GAMEOVER = False

    global MYCOLOR
    MYCOLOR = pygame.Color(10, 100, 255, 255)

    pygame.display.set_caption('CHASE!')

pygame.init()

DISPLAYSURF = pygame.display.set_mode((width, height))

pygame.display.set_caption('CHASE!')

MYCOLOR = pygame.Color(10, 100, 255, 255)
RED = pygame.Color(255, 25, 25)
BLACK = pygame.Color(0, 0, 0)
DISPLAYSURF.fill(MYCOLOR)

obstacle_scale = 8000
num_obstacles = (width * height) / obstacle_scale

circles = loadCircles(num_obstacles)

p_x = 0
p_y = 0
p_radius = 10

e_x = width
e_y = height
e_radius = 10

p_speed = .5
e_speed = .2

left = False
right = False
up = False
down = False
dip = True
slope = 0

GAMEOVER = False

while True:
    DISPLAYSURF.fill(MYCOLOR)
    pygame.draw.circle(DISPLAYSURF, RED, (int(p_x), int(p_y)), p_radius, 0) # player
    drawCircles(DISPLAYSURF, circles, not GAMEOVER) # obstacles
    pygame.draw.circle(DISPLAYSURF, BLACK, (int(e_x), int(e_y)), e_radius, 0) # enemy

    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if not GAMEOVER:
            if pressed[pygame.K_UP]:
                up = True
            else:
                up = False
            if pressed[pygame.K_DOWN]:
                down = True
            else:
                down = False
            if pressed[pygame.K_LEFT]:
                left = True
            else:
                left = False
            if pressed[pygame.K_RIGHT]:
                right = True
            else:
                right = False

        if GAMEOVER:
            if pressed[pygame.K_RETURN]:
                reset()

    if not GAMEOVER:
        distance_x = p_x - e_x
        distance_y = e_y - p_y

        if distance_x < 0.001 and distance_x > -0.001:
            if distance_y > 0:
                slope = -float("inf")
            else:
                slope = float("inf")
        else:
            slope = distance_y / distance_x

        if slope == float("inf"):
            e_y += e_speed
        elif slope == -float("inf"):
            e_y -= e_speed
        else:

            x_inc = e_speed * math.cos(math.atan(slope))
            y_inc = e_speed * math.sin(math.atan(slope))

            if distance_x < 0:
                e_x -= x_inc
                if distance_x > -0.001:
                    e_y -= y_inc
                else:
                    e_y += y_inc
            else:
                e_x += x_inc
                if distance_x < 0.001:
                    e_y += y_inc
                else:
                    e_y -= y_inc

        x_diag = p_speed * math.cos(math.pi / 4)
        y_diag = p_speed * math.sin(math.pi / 4)

        if up:
            if right:
                p_y -= y_diag
                p_x += x_diag
            elif left:
                p_y -= y_diag
                p_x -= x_diag
            else:
                p_y -= p_speed
        elif down:
            if right:
                p_y += y_diag
                p_x += x_diag
            elif left:
                p_y += y_diag
                p_x -= x_diag
            else:
                p_y += p_speed
        elif left:
            p_x -= p_speed
        elif right:
            p_x += p_speed

        if e_x > width:
            e_x = width
        if e_x < 0:
            e_x = 0
        if p_x > width:
            p_x = width
        if p_x < 0:
            p_x = 0
        if e_y > height:
            e_y = height
        if e_y < 0:
            e_y = 0
        if p_y > height:
            p_y = height
        if p_y < 0:
            p_y = 0

        distance = math.sqrt(distance_x * distance_x + distance_y * distance_y)

        collided = False
        if distance < p_radius + e_radius: # collision
            collided = True

        for obstacle in circles:
            d_x = p_x - obstacle.x
            d_y = p_y - obstacle.y
            distance = math.sqrt(d_x * d_x + d_y * d_y)
            if distance < p_radius + obstacle.radius: # collision
                collided = True

        if collided:
            MYCOLOR = pygame.Color(25, 255, 100, 255)
            GAMEOVER = True
            pygame.display.set_caption('GAMEOVER! Press ENTER to restart')

    pygame.display.update()
