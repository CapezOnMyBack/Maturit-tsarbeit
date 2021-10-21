import pygame
from config import get_Asset as gA
from pygame.locals import *


# settings
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
vec = pygame.math.Vector2
max_speed = 5
dt = 0
count = False
perm_dt = 1
pink = (153, 0, 153)
blue = (56, 165, 255)
distance = 0

# FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, bool(1), pygame.Color("coral"))
    return fps_text


# def update_timer():
    # global time_original
    # if car.touch_line == 0:
        # time_original = ((car.roundtime - car.time)/1000)
    # time = str(time_original)
    # time_text = font.render(time, bool(1), pygame.Color("coral"))
    # return time_text


# sprite(s)
class Car(pygame.sprite.Sprite):
    def __init__(self, n):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(gA("car_2.png")).convert_alpha()
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
        self.distance_f = (0.0, 0.0)
        self.distance_R = (0.0, 0.0)
        self.distance_L = (0.0, 0.0)
        self.distance_f_R = (0.0, 0.0)
        self.distance_f_L = (0.0, 0.0)
        self.mask_R = pygame.mask.from_surface(pygame.image.load(gA("rennstrecke_rand.png")).convert_alpha())
        self.n = n
        self.death_time = 0
        self.goright = 0
        self.goleft = 0

    def __repr__(self):
        return f'<Car({self.n})>'

    def __str__(self):
        return self.__repr__()

    #---------------------------------------------------------------------------------------------------------
    #SENSOR FUNCTIONS:

    def sensor_front(self):

        for distance_multiplier in range(1, 80):
            self.distance_f = (self.position + 1.5 ** (distance_multiplier/6) * self.vel)
            pos_x = abs(int(self.distance_f[0]))
            pos_y = abs(int(self.distance_f[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_front_R(self):

        for distance_multiplier in range(1, 80):
            self.distance_f_R = (self.position + 1.5 ** (distance_multiplier/6) * self.vel.rotate(30))
            pos_x = abs(int(self.distance_f_R[0]))
            pos_y = abs(int(self.distance_f_R[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_front_L(self):

        for distance_multiplier in range(1, 80):
            self.distance_f_L = (self.position + 1.5 ** (distance_multiplier/6) * self.vel.rotate(-30))
            pos_x = abs(int(self.distance_f_L[0]))
            pos_y = abs(int(self.distance_f_L[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_back_R(self):

        for distance_multiplier in range(1, 80):
            self.distance_R = ((self.position - 4 * self.vel) + 1.5 ** (distance_multiplier/6) * self.vel.rotate(90))
            pos_x = abs(int(self.distance_R[0]))
            pos_y = abs(int(self.distance_R[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_back_L(self):

        for distance_multiplier in range(1, 80):
            self.distance_L = ((self.position - 4 * self.vel) + 1.5 ** (distance_multiplier/6) * self.vel.rotate(-90))
            pos_x = abs(int(self.distance_L[0]))
            pos_y = abs(int(self.distance_L[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    #------------------------------------------------------------------------------------------------
    #DISTANCE TEXT UPDATES:

    def update_distance_f(self):
        value_distance_f = str(round((abs((self.distance_f - self.position).length()) / 100), 2))
        value_distance_f_text = font.render(value_distance_f , bool(1), pygame.Color("coral"))

        return value_distance_f_text

    def update_distance_f_R(self):

        value_distance_f_R = str(round((abs((self.distance_f_R - self.position).length()) / 100), 2))
        value_distance_f_R_text = font.render(value_distance_f_R, bool(1), pygame.Color("coral"))

        return value_distance_f_R_text

    def update_distance_f_L(self):

        value_distance_f_L = str(round((abs((self.distance_f_L - self.position).length()) / 100), 2))
        value_distance_L_text = font.render(value_distance_f_L, bool(1), pygame.Color("coral"))

        return value_distance_L_text

    def update_distance_b_R(self):

        value_distance_b_R = str(round((abs((self.distance_R - (self.position - 4 * self.vel)).length()) / 100), 2))
        value_distance_b_R_text = font.render(value_distance_b_R, bool(1), pygame.Color("coral"))

        return value_distance_b_R_text

    def update_distance_b_L(self):

        value_distance_b_L = str(round((abs((self.distance_L - (self.position - 4 * self.vel)).length()) / 100), 2))
        value_distance_b_L_text = font.render(value_distance_b_L, bool(1), pygame.Color("coral"))

        return value_distance_b_L_text

    #--------------------------------------------------------------------------------------------------------

    #def update_death_time(self, self.death_time):

        #death_time_val = str(self.death_time / 1000)
        #death_time_text = font.render(death_time_val, bool(1), pygame.Color("coral"))
        #return death_time_text

    def update(self):
        global count
        keys = pygame.key.get_pressed()
        if self.perm:
            if keys[K_a] or self.goleft == 1:
                self.angle_speed = -4
                self.rotate()
                self.goleft = 0
            if keys[K_d] or self.goright == 1:
                self.angle_speed = 4
                self.rotate()
                self.goright = 0
            if not keys[K_w]:
                self.vel += self.acceleration
                if not count:
                    self.time = pygame.time.get_ticks()
                    count = True
            if keys[K_w]:
                self.vel = vec(0, 0)

        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)

        self.position += self.vel * (self.n * 0.4)
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

        self.col_line = pygame.sprite.collide_mask(Car, Ziel)
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
        self.col_pos = pygame.sprite.collide_mask(Rand, Car)
        if self.col_pos is not None:
            self.perm = False
            self.vel = vec(0, 0)
            if perm_dt == 1:
                dt = 1
                self.death_time = pygame.time.get_ticks()
                perm_dt -= 1


class Rand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(gA("rennstrecke_rand.png")).convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Ziel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(gA("rennstrecke_ziel.png")).convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


