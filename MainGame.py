import pygame
from pygame.locals import *


# settings
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
vec = pygame.math.Vector2
max_speed = 5
perm = True
dt = 0
count = False
death_time = 0
perm_dt = 1
pink = (153, 0, 153)
distance = 0

# FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, bool(1), pygame.Color("coral"))
    return fps_text


def update_timer():
    global time_original
    if car.touch_line == 0:
        time_original = ((car.roundtime - car.time)/1000)
    time = str(time_original)
    time_text = font.render(time, bool(1), pygame.Color("coral"))
    return time_text

# collision

def collision():
    global perm_dt
    global dt
    global perm
    global death_time
    global col_pos
    col_pos = pygame.sprite.collide_mask(rand, car)
    if col_pos != None:
        perm = False
        car.vel = vec(0, 0)
        if perm_dt == 1:
            dt = 1
            death_time = pygame.time.get_ticks()
            perm_dt -= 1


def update_death_time(death_time):
    death_time_val = str(death_time/1000)
    death_time_text = font.render(death_time_val, bool(1), pygame.Color("coral"))
    return death_time_text

# sprite
class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/aleks/Desktop/car_2.png").convert_alpha()
        self.original_image = self.image
        self.position = vec(638, 440)
        self.rect = self.original_image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(2, 0)
        self.angle_speed = 0
        self.angle = 0
        self.time = 0
        self.roundtime = 0
        self.touch_line = 0
        self.col_line = None


    def update(self):
        global count
        keys = pygame.key.get_pressed()
        if perm == True:
            if keys[K_a]:
                self.angle_speed = -4
                car.rotate()
            if keys[K_d]:
                self.angle_speed = 4
                car.rotate()
            if keys[K_w]:
                self.vel += self.acceleration
                if count == False:
                    self.time = pygame.time.get_ticks()
                    count = True
            if not keys[K_w]:
                self.vel = vec(0, 0)

        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):

        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def touchfl(self):

        self.col_line = pygame.sprite.collide_mask(car, ziel)
        if self.touch_line == 0:
            if self.col_line != None:
                self.touch_line = 1
        if self.touch_line == 1:
            if self.col_line == None:
                self.touch_line = 0

    def timecount(self):

        if self.touch_line == 1:
            self.roundtime = pygame.time.get_ticks()


class Sensor_s(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/aleks/Desktop/sensor_straight.png").convert_alpha()
        self.original_image = self.image
        self.position = car.position
        self.rect = self.original_image.get_rect(center=self.position)

    def update(self):
        self.position = car.position
        self.rect.center = self.position

        self.image = pygame.transform.rotate(self.original_image, -car.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

class Rand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/aleks/Desktop/rennstrecke_rand.png").convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Ziel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Users/aleks/Desktop/rennstrecke_ziel.png").convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

def distance_sensor_s():
    global distance
    global vec_sensor_s
    vec_sensor_s = (car.position + pygame.sprite.collide_mask(car, sensor_s)) - (pygame.sprite.collide_mask(rand, sensor_s))
    distance = vec_sensor_s.length()


strecke = pygame.image.load("C:/Users/aleks/Desktop/rennstrecke.png").convert_alpha()
all_sprites = pygame.sprite.Group()
car = Car()
rand = Rand()
sensor_s = Sensor_s()
ziel = Ziel()
all_sprites.add(ziel, sensor_s, rand, car)

# engine
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    collision()
    all_sprites.update()
    car.touchfl()
    car.timecount()

    screen.blit(strecke, (0, 0))
    all_sprites.draw(screen)
    if col_pos != None:
        pygame.draw.line(screen, pink, (0, 0), col_pos, width = 2)
    if pygame.sprite.collide_mask(car, sensor_s) != None:
        pygame.draw.line(screen, pink, (0, 0), pygame.sprite.collide_mask(car, sensor_s), width=2)
    if pygame.sprite.collide_mask(rand, sensor_s) != None:
        pygame.draw.line(screen, pink, (0, 0), pygame.sprite.collide_mask(rand, sensor_s), width = 2)
    distance_sensor_s()
    screen.blit(update_fps(), (10, 10))
    screen.blit(update_death_time(death_time), (10, 50))
    screen.blit(update_timer(), (10, 30))
    pygame.display.set_caption('vel {:.1f}'.format((car.vel.length()/5)*100))
    #print(distance)
    print(pygame.sprite.collide_mask(car, sensor_s))
    pygame.display.update()

    clock.tick(60)