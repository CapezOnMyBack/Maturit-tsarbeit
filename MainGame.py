import pygame
from config import asset_path as ap
from pygame.locals import *


# settings
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
vec = pygame.math.Vector2
max_speed = 5
dt = 0
count = False
death_time = 0
perm_dt = 1
pink = (153, 0, 153)
blue = (176, 120, 230)
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


# sprite
class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ap.joinpath("car_2.png")).convert_alpha()
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
        self.perm = True
        self.sensor_hit = (0, 0)

        #pygame.draw.line(screen, blue, (car.position), (car.position + 30 * car.vel), width=2)

    def sensor_front(self):
        mask_R = pygame.mask.from_surface(pygame.image.load(ap.joinpath("rennstrecke_rand.png")).convert_alpha())

        for distance_multiplier in range(1, 129):
            self.distance_pos = (self.position + 1.05 ** distance_multiplier * car.vel)
            pos_x = abs(int(self.distance_pos[0]))
            pos_y = abs(int(self.distance_pos[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:

                break

    def update_death_time(self, death_time):
        death_time_val = str(death_time / 1000)
        death_time_text = font.render(death_time_val, bool(1), pygame.Color("coral"))
        return death_time_text

    def update(self):
        global count
        keys = pygame.key.get_pressed()
        if self.perm:
            if keys[K_a]:
                self.angle_speed = -4
                self.rotate()
            if keys[K_d]:
                self.angle_speed = 4
                self.rotate()
            if keys[K_w]:
                self.vel += self.acceleration
                if not count:
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

    def collision(self):
        global perm_dt
        global dt
        global death_time
        self.col_pos = pygame.sprite.collide_mask(rand, car)
        if self.col_pos is not None:
            self.perm = False
            car.vel = vec(0, 0)
            if perm_dt == 1:
                dt = 1
                death_time = pygame.time.get_ticks()
                perm_dt -= 1

#mit dem auto:

class Rand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ap.joinpath("rennstrecke_rand.png")).convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Ziel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ap.joinpath("rennstrecke_ziel.png")).convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)



strecke = pygame.image.load(ap.joinpath("rennstrecke.png")).convert_alpha()
all_sprites = pygame.sprite.Group()
car = Car()
rand = Rand()
ziel = Ziel()
all_sprites.add(ziel, rand, car)

# engine
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    car.collision()
    all_sprites.update()
    car.touchfl()
    car.timecount()
    car.sensor_front()

    screen.blit(strecke, (0, 0))
    all_sprites.draw(screen)
    if car.col_pos != None:
        pygame.draw.line(screen, pink, (0, 0), car.col_pos, width = 2)

    pygame.draw.line(screen, blue, (car.position), (car.distance_pos) , width=2)

    screen.blit(update_fps(), (10, 10))
    screen.blit(car.update_death_time(death_time), (10, 50))
    screen.blit(update_timer(), (10, 30))
    pygame.display.set_caption('Alex Maturarbeit')
    pygame.display.update()

    clock.tick(60)