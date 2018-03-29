import pygame, sys, math, random, time, re, os
from pygame.locals import *
from vector3D import vector3D

# Define Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
PURPLE = pygame.Color(255, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

WIDTH = 400
HEIGHT = 300
GAMEOVER = False
BACKGROUND = GREEN
GLOBAL_SPEED_MODIFIER = 0

def main():
    global WIDTH
    global HEIGHT
    global GAMEOVER
    global BACKGROUND

    # get sounds files in dir
    songs = []
    WAV = re.compile(".+\.wav")
    OGG = re.compile(".+\.ogg")
    MP3 = re.compile(".+\.mp3")
    for file in os.listdir("."):
        if WAV.match(file) or OGG.match(file) or MP3.match(file):
            songs.append(file)

    response = raw_input("Set screen? (y/n)").lower()

    if response == "y":

        passed = False

        WIDTH = raw_input("Width = ")
        while not passed:
            try:
                WIDTH = int(WIDTH)
                passed = True
            except:
                WIDTH = raw_input("Width = ")

        passed = False

        HEIGHT = raw_input("Height = ")
        while not passed:
            try:
                HEIGHT = int(HEIGHT)
                passed = True
            except:
                HEIGHT = raw_input("Height = ")

    # user_name = raw_input("What is your username? ")
    # time_log = open(user_name + "_time_log.txt","w+")
    try:
        time_log = open("time_log.txt","r+")
    except:
        time_log = open("time_log.txt","w+")

    passed = False

    FPS = raw_input("FPS = ")
    if FPS == "":
        passed = True
        FPS = 30
    while not passed:
        try:
            FPS = int(FPS)
            passed = True
        except:
            HEIGHT = raw_input("FPS = ")

    print "Which song would you like in the background?\n"

    for i in range(len(songs)):
        song_number = i + 1
        print str(song_number) + ": " + songs[i]

    passed = False

    song_index = raw_input("Enter the number for your choice: ")
    song = ""
    if song_index == "":
        passed = True
        song = ".ChaseGameMusic.wav"
    while not passed:
        try:
            song_index = int(song_index)
            song = songs[song_index - 1]
            if song_index > 0 and song_index <= len(songs):
                passed = True
            else:
                song_index = raw_input("Enter the number for your choice: ")
        except:
            song_index = raw_input("Enter the number for your choice: ")

    # prior to fps counter
    # GLOBAL_SPEED_MODIFIER = (WIDTH * HEIGHT) / 120000
    # 30 fps, high difficulty 60
    # GLOBAL_SPEED_MODIFIER = (WIDTH * HEIGHT) / 12000
    # current 60 = 18000
    # current 15 = 24000
    fps_scale = 2400 * int(math.sqrt(FPS))
    GLOBAL_SPEED_MODIFIER = (WIDTH * HEIGHT) / fps_scale

    obstacle_scale = 8000
    num_obstacles = (WIDTH * HEIGHT) / obstacle_scale

    obstacles = loadCircles(num_obstacles, GLOBAL_SPEED_MODIFIER)

    player_default = .3

    PLAYER = player(vector3D(), vector3D(), vector3D(), 0, 10, \
                    player_default * GLOBAL_SPEED_MODIFIER)

    ENEMY = enemy(vector3D(WIDTH, HEIGHT, 0), vector3D(), vector3D(), \
                    0, 10, .2 * GLOBAL_SPEED_MODIFIER)

    POWER_UP = power_up(vector3D(), vector3D(), vector3D(), 0, 8, .05, YELLOW)

    BACKGROUND = GREEN

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('CHASE!')

    pygame.mixer.init(22050, -16, 2, 4096)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)

    # DrawWorld(DISPLAYSURF, BACKGROUND, PLAYER, ENEMY, obstacles, power_up)
    enemy_speed_up = time.time()

    power_up_spawn = time.time()
    power_up_fast = 3
    power_up_slow = 6
    power_up_respawn = random.randrange(power_up_fast, power_up_slow)

    run_time = time.time()

    times_list = []

    time_add = False

    while True:

        DrawWorld(DISPLAYSURF, BACKGROUND, PLAYER, ENEMY, obstacles, POWER_UP)

        cur_time = time.time()
        if cur_time > enemy_speed_up + 10:
            enemy_speed_up = cur_time
            ENEMY.speed += .05 * GLOBAL_SPEED_MODIFIER

        if not POWER_UP.available:
            if cur_time > power_up_spawn + power_up_respawn:
                POWER_UP.position = vector3D(random.randrange(0, WIDTH), \
                    random.randrange(0, HEIGHT), 0)
                POWER_UP.velocity = vector3D(random.randrange(-30, 31), \
                    random.randrange(-30, 31), 0)
                POWER_UP.available = True
                power_up_spawn = cur_time
                power_up_respawn = random.randrange(power_up_fast, power_up_slow)

        if GAMEOVER and not time_add:
            times_list.append(time.time() - run_time)
            time_add = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ExitGame(DISPLAYSURF, times_list, time_log)

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_ESCAPE]:
                ExitGame(DISPLAYSURF, times_list, time_log)

            if GAMEOVER:

                if pressed[pygame.K_RETURN]:
                    # reset everything to initial world start
                    obstacles = loadCircles(num_obstacles, GLOBAL_SPEED_MODIFIER)
                    PLAYER.position = vector3D()
                    PLAYER.velocity = vector3D()
                    ENEMY.position.x = WIDTH
                    ENEMY.position.y = HEIGHT
                    PLAYER.velocity = vector3D()
                    PLAYER.update_speed(player_default * GLOBAL_SPEED_MODIFIER)
                    BACKGROUND = GREEN
                    enemy_speed_up = time.time()
                    ENEMY.speed = .2 * GLOBAL_SPEED_MODIFIER
                    POWER_UP.available = False
                    power_up_spawn = time.time()
                    power_up_respawn = random.randrange(power_up_fast, power_up_slow)
                    run_time = time.time()
                    time_add = False
                    pygame.display.set_caption('CHASE! %10f' % (time.time() - run_time))
                    GAMEOVER = False

            if not GAMEOVER:
                if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                    up = True
                else:
                    up = False
                if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                    down = True
                else:
                    down = False
                if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                    left = True
                else:
                    left = False
                if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                    right = True
                else:
                    right = False

        if not GAMEOVER:
            PLAYER.velocity.x = 0
            PLAYER.velocity.y = 0
            if up:
                PLAYER.velocity.y += 1
            if down:
                PLAYER.velocity.y += -1
            if right:
                PLAYER.velocity.x += 1
            if left:
                PLAYER.velocity.x += -1

            pygame.display.set_caption('CHASE! %5f' % (time.time() - run_time))
            WorldUpdate(DISPLAYSURF, PLAYER, ENEMY, obstacles, POWER_UP, \
                (time.time() - run_time), GLOBAL_SPEED_MODIFIER)

        pygame.time.Clock().tick(FPS)

def ExitGame(surf, times_list, log):
    surf.fill(WHITE)
    for line in log:
        time_val = 0
        is_val = True
        try:
            time_val = float(line)
        except:
            is_val = False

        if is_val and time_val not in times_list:
            times_list.append(time_val)

    log = open("time_log.txt", "r+")

    list_index = 1
    times_list = sorted(times_list)
    while list_index <= 10 and list_index <= len(times_list):
        log.write(str(times_list[-(list_index)]) + "\n")
        list_index += 1
    log.close()
    pygame.quit()
    sys.exit()

def loadCircles(num_obstacles, GLOBAL_SPEED_MODIFIER):
    list = []
    for i in range(num_obstacles):
        temp_pos = vector3D(random.randrange(0, WIDTH), \
            random.randrange(0, HEIGHT), 0)

        while temp_pos.x < 100 and temp_pos.y < 100:
            temp_pos = vector3D(random.randrange(0, WIDTH), \
                random.randrange(0, HEIGHT), 0)

        o = obstacle(temp_pos, vector3D(random.randrange(-30, 31), \
            random.randrange(-30, 31), 0), vector3D(), 0, 5, \
            .1 * GLOBAL_SPEED_MODIFIER)
        list.append(o)
    return list

def DrawWorld(surf, BACKGROUND, player, enemy, obstacles, power_up):
    surf.fill(BACKGROUND)
    # player
    pygame.draw.circle(surf, player.color, (int(player.position.x), \
        int(player.position.y)), player.radius, 0)
    # power up
    if power_up.available:
        pygame.draw.circle(surf, power_up.color, (int(power_up.position.x), \
            int(power_up.position.y)), power_up.radius, 0)
    # obstacles
    for ob in obstacles:
        pygame.draw.circle(surf, ob.color, (int(ob.position.x), \
            int(ob.position.y)), ob.radius, 0)
    # enemy
    pygame.draw.circle(surf, enemy.color, (int(enemy.position.x), \
        int(enemy.position.y)), enemy.radius, 0)


def WorldUpdate(surf, player, enemy, obstacles, power_up, run_time, GLOBAL_SPEED_MODIFIER):
    for ob in obstacles:
        ob.update()
    player.update()
    enemy.update(player)
    if power_up.available:
        distance = math.sqrt((player.position.x - power_up.position.x)**2 \
                + (player.position.y - power_up.position.y)**2)
        if distance < player.radius + power_up.radius: # collision
            player.update_speed(player.speed + (.025 * GLOBAL_SPEED_MODIFIER))
            power_up.available = False
        power_up.update()
    global GAMEOVER
    global BACKGROUND
    if collision(player, enemy, obstacles):
        BACKGROUND = WHITE
        GAMEOVER = True
        pygame.display.set_caption('GAMEOVER! %5f  Press ENTER to restart' % (run_time))
        DrawWorld(surf, BACKGROUND, player, enemy, obstacles, power_up)
    pygame.display.update()

def collision(player, enemy, obstacles):
    distance = math.sqrt((player.position.x - enemy.position.x)**2 + \
                            (player.position.y - enemy.position.y)**2)
    if distance < player.radius + enemy.radius: # collision
        return True

    for obstacle in obstacles:
        d_x = player.position.x - obstacle.position.x
        d_y = player.position.y - obstacle.position.y
        distance = math.sqrt(d_x * d_x + d_y * d_y)
        if distance < player.radius + obstacle.radius - 1: # collision
            return True
    return False

class obj:
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=(), mass=0):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()

    def update(self, speed):
        self.update_pos(speed)

    def update_pos(self, speed):
        self.position.x += self.direction.x * speed
        self.position.y += self.direction.y * speed
        self.position.z += self.direction.z * speed

class circ(obj):
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=vector3D(), mass=0, radius=1, speed=0, color=BLACK):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.update_pos(self.speed)

    def update_pos(self, speed):
        self.direction = self.velocity.unit_vector()
        self.position.x += self.direction.x * self.speed
        self.position.y -= self.direction.y * self.speed
        if self.position.x > WIDTH:
            self.position.x = WIDTH
        if self.position.x < 0:
            self.position.x = 0
        if self.position.y > HEIGHT:
            self.position.y = HEIGHT
        if self.position.y < 0:
            self.position.y = 0

class player(circ):
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=vector3D(), mass=0, radius=1, speed=0, color=RED):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.update_pos()

    def update_speed(self, val):
        self.speed = val

    def update_pos(self):
        self.direction = self.velocity.unit_vector()
        self.position.x += self.direction.x * self.speed
        self.position.y -= self.direction.y * self.speed
        if self.position.x > WIDTH:
            self.position.x = WIDTH
        if self.position.x < 0:
            self.position.x = 0
        if self.position.y > HEIGHT:
            self.position.y = HEIGHT
        if self.position.y < 0:
            self.position.y = 0

class enemy(circ):
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=vector3D(), mass=0, radius=1, speed=0, color=BLACK):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self, player):
        self.update_velocity(player)
        self.update_pos()

    def update_velocity(self, player):
        self.velocity = player.position - self.position
        self.direction = self.velocity.unit_vector()

    def update_pos(self):
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed
        if self.position.x > WIDTH:
            self.position.x = WIDTH
        if self.position.x < 0:
            self.position.x = 0
        if self.position.y > HEIGHT:
            self.position.y = HEIGHT
        if self.position.y < 0:
            self.position.y = 0

class obstacle(circ):
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=vector3D(), mass=0, radius=1, speed=0, color=PURPLE):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.update_pos()

    def update_pos(self):
        if self.position.x + self.radius > WIDTH or \
            self.position.x - self.radius < 0:
            self.velocity.x = self.velocity.x * -1
        if self.position.y + self.radius > HEIGHT or \
            self.position.y - self.radius < 0:
            self.velocity.y = self.velocity.y * -1
        self.direction = self.velocity.unit_vector()
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed

class power_up(circ):
    def __init__(self, position=vector3D(), velocity=vector3D(), \
    acceleration=vector3D(), mass=0, radius=1, speed=0, color=YELLOW, \
    available=False):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.force = acceleration * mass
        self.direction = velocity.unit_vector()
        self.radius = radius
        self.speed = speed
        self.color = color
        self.available = available

    def update(self):
        self.update_pos(self.speed)

    def update_pos(self, speed):
        if self.position.x + self.radius > WIDTH or \
            self.position.x - self.radius < 0:
            self.velocity.x = self.velocity.x * -1
        if self.position.y + self.radius > HEIGHT or \
            self.position.y - self.radius < 0:
            self.velocity.y = self.velocity.y * -1
        self.direction = self.velocity.unit_vector()
        self.position.x += self.direction.x * self.speed
        self.position.y += self.direction.y * self.speed

main()
