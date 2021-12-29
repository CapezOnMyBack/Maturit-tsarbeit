import numpy as np
import pygame
from config import get_Asset as gA, ai_control
from pygame.locals import *
from BetterNN import Network


# settings
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
vec = pygame.math.Vector2
max_speed = 5
pink = (153, 0, 153)
blue = (56, 165, 255)
distance = 0
global_dt = 0


# FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
font_2 = pygame.font.SysFont("Arial", 25)


# sprite(s)
class Car(pygame.sprite.Sprite):

    def __init__(self, n, rand, ziel, network: Network):
        pygame.sprite.Sprite.__init__(self)
        self.rand = rand
        self.ziel = ziel
        self.image = pygame.image.load(gA("auto.png")).convert_alpha()
        self.original_image = self.image
        self.position = vec(570, 450)
        self.rect = self.original_image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(2, 0)
        self.angle_speed = 0
        self.angle = 0
        self.time = 0
        self.roundtime = 0
        self.touch_line = False
        self.single_tl_output = False
        self.perm = True
        self.sensor_f_hit = vec(0.0, 0.0)
        self.sensor_R_hit = vec(0.0, 0.0)
        self.sensor_L_hit = vec(0.0, 0.0)
        self.sensor_f_R_hit = vec(0.0, 0.0)
        self.sensor_f_L_hit = vec(0.0, 0.0)
        self.sensor_s_R_hit = vec(0.0, 0.0)
        self.sensor_s_L_hit = vec(0.0, 0.0)
        self.mask_R = pygame.mask.from_surface(pygame.image.load(gA("rennstrecke_rand_grass.png")).convert_alpha())
        self.n = n
        self.death_time = 0
        self.time_alive = 0
        self.goright = 0
        self.goleft = 0
        self.alive = True
        self.network = network
        self.perm_dt = True
        self.count = False

    def __repr__(self):
        return f'<Car({self.n})>'

    def __str__(self):
        return self.__repr__()

    # ---------------------------------------------------------------------------------------------------------
    # SENSOR FUNCTIONS:

    def sensor_front(self):

        for distance_multiplier in range(1, 80):
            self.sensor_f_hit = (self.position + 1.5 ** (distance_multiplier / 6) * self.vel)
            pos_x = abs(int(self.sensor_f_hit[0]))
            pos_y = abs(int(self.sensor_f_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_front_R(self):

        for distance_multiplier in range(1, 80):
            self.sensor_f_R_hit = (self.position + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(30))
            pos_x = abs(int(self.sensor_f_R_hit[0]))
            pos_y = abs(int(self.sensor_f_R_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_front_L(self):

        for distance_multiplier in range(1, 80):
            self.sensor_f_L_hit = (self.position + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(-30))
            pos_x = abs(int(self.sensor_f_L_hit[0]))
            pos_y = abs(int(self.sensor_f_L_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_side_R(self):

        for distance_multiplier in range(1, 80):
            self.sensor_s_R_hit = (self.position + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(50))
            pos_x = abs(int(self.sensor_s_R_hit[0]))
            pos_y = abs(int(self.sensor_s_R_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_side_L(self):

        for distance_multiplier in range(1, 80):
            self.sensor_s_L_hit = (self.position + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(-50))
            pos_x = abs(int(self.sensor_s_L_hit[0]))
            pos_y = abs(int(self.sensor_s_L_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_back_R(self):

        for distance_multiplier in range(1, 80):
            self.sensor_R_hit = (self.position
                                 + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(90))
            pos_x = abs(int(self.sensor_R_hit[0]))
            pos_y = abs(int(self.sensor_R_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    def sensor_back_L(self):

        for distance_multiplier in range(1, 80):
            self.sensor_L_hit = (self.position
                                 + 1.5 ** (distance_multiplier / 6) * self.vel.rotate(-90))
            pos_x = abs(int(self.sensor_L_hit[0]))
            pos_y = abs(int(self.sensor_L_hit[1]))
            if pos_x >= 1279:
                pos_x = 1279
            if pos_y >= 719:
                pos_y = 719
            sensor_hit = self.mask_R.get_at((pos_x, pos_y))

            if sensor_hit == 1:
                break

    # ------------------------------------------------------------------------------------------------
    # DISTANCE TEXT UPDATES:

    def update_distance_f(self):
        value_distance_f = str(round((abs((self.sensor_f_hit - self.position).length()) / 100), 2))
        value_distance_f_text = font.render(value_distance_f, bool(1), pygame.Color("coral"))

        return value_distance_f_text

    def update_distance_f_R(self):

        value_distance_f_R = str(round((abs((self.sensor_f_R_hit - self.position).length()) / 100), 2))
        value_distance_f_R_text = font.render(value_distance_f_R, bool(1), pygame.Color("coral"))

        return value_distance_f_R_text

    def update_distance_f_L(self):

        value_distance_f_L = str(round((abs((self.sensor_f_L_hit - self.position).length()) / 100), 2))
        value_distance_L_text = font.render(value_distance_f_L, bool(1), pygame.Color("coral"))

        return value_distance_L_text

    def update_distance_b_R(self):

        value_distance_b_R = str(round((abs((self.sensor_R_hit - (self.position - 4 * self.vel)).length()) / 100), 2))
        value_distance_b_R_text = font.render(value_distance_b_R, bool(1), pygame.Color("coral"))

        return value_distance_b_R_text

    def update_distance_b_L(self):

        value_distance_b_L = str(round((abs((self.sensor_L_hit - (self.position - 4 * self.vel)).length()) / 100), 2))
        value_distance_b_L_text = font.render(value_distance_b_L, bool(1), pygame.Color("coral"))

        return value_distance_b_L_text

    # --------------------------------------------------------------------------------------------------------

    def update_alive_timer(self):

        alive_time_val = f'Survival Time:{str(self.time_alive)}'
        alive_time_text = font_2.render(alive_time_val, bool(1), pygame.Color("black"))
        return alive_time_text
    # --------------------------------------------------------------------------------------------------------

    def calc_distances(self) -> np.ndarray:
        input_1 = (self.sensor_f_hit - self.position).length()
        input_2 = (self.sensor_f_R_hit - self.position).length()
        input_3 = (self.sensor_f_L_hit - self.position).length()
        input_4 = (self.sensor_s_R_hit - self.position).length()
        input_5 = (self.sensor_s_L_hit - self.position).length()
        input_6 = (self.sensor_R_hit - self.position).length()
        input_7 = (self.sensor_L_hit - self.position).length()
        return np.array([input_1, input_2, input_3, input_4, input_5, input_6, input_7]) / 100

    # --------------------------------------------------------------------------------------------------------

    def direction_decision(self):

        activations = self.calc_distances()
        output = self.network.forward(activations=activations)

        if output.argmax() == 0:
            self.goright = 1
            self.goleft = 0
        elif output.argmax() == 1:
            self.goright = 0
            self.goleft = 1
        elif output.argmax() == 2:
            self.goright = 0
            self.goleft = 0

    # --------------------------------------------------------------------------------------------------------

    def update(self, frames):

        self.sensor_front()
        self.sensor_back_R()
        self.sensor_back_L()
        self.sensor_side_R()
        self.sensor_side_L()
        self.sensor_front_R()
        self.sensor_front_L()

        if ai_control:
            self.direction_decision()

        self.collision(frames)
        self.touchfl()
        self.timecount(frames)
        self.alive_time(frames)

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
                if not self.count:
                    self.time = pygame.time.get_ticks()
                    self.count = True
            if keys[K_w]:
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

    # When touching the finishline, give ONE single output

        if pygame.sprite.collide_mask(self, self.ziel) is not None:
            self.single_tl_output = True
            self.touch_line = True
        elif pygame.sprite.collide_mask(self, self.ziel) is None:
            self.touch_line = False

    def alive_time(self, frames):

        self.time_alive = round(((frames / 60) - self.death_time), 3)

    def timecount(self, frames):

        if self.touch_line:
            self.roundtime = frames

    def collision(self, frames):
        global global_dt
        self.col_pos = pygame.sprite.collide_mask(self.rand, self)
        if self.col_pos is not None:
            self.perm = False
            self.vel = vec(0, 0)
            if self.perm_dt:
                self.death_time = frames / 60
                global_dt = self.death_time
                self.alive = False
                self.perm_dt = False


class Border(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(gA("rennstrecke_rand_grass.png")).convert_alpha()
        self.position = vec(0, 0)
        self.original_image = self.image
        self.rect = self.original_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Ziel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(gA("rennstrecke_ziel.png")).convert_alpha()
        self.x = 0
        self.y = 0
        self.original_image = self.image
        self.rect = self.original_image.get_rect(top=self.y, left=self.x)
        self.mask = pygame.mask.from_surface(self.image)
