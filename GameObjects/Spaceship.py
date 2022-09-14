import json
import pygame
from pymunk import Body, Poly, Circle
from math import cos, sin, degrees, radians, dist, atan2
from GameObjects import Asteroid, Decoration
from random import choice, randint
from os import listdir


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, space, position, json_file, angle=90):

        super().__init__()
        self.read_from_json(json_file)

        # pymunk init

        self.space = space
        self.body = Body()
        self.body.position = position
        self.body.angle += radians(-angle)

        self.main_engine_on = False
        self.side_engine_on = False

        # pygame init

        self.original_image = pygame.image.load(self.image).convert_alpha()
        self.original_image = pygame.transform.smoothscale(
            self.original_image, self.image_size)
        self.rect = self.original_image.get_rect(center=self.body.position)

        # pymunk init

        self.shapes = []
        shape = Circle(self.body, 20)
        shape.mass = self.polygons[0]["mass"]
        shape.elasticity = self.polygons[0]["elasticity"]
        shape.friction = self.polygons[0]["friction"]
        self.shapes.append(shape)
        for poly in self.polygons:

            poly["vertices"] = list(
                map(lambda x: [x[0]/(300/self.image_size[0]), x[1]/(300/self.image_size[0])], poly["vertices"]))

            shape = Poly(self.body, poly["vertices"])
            shape.mass = poly["mass"]
            shape.elasticity = poly["elasticity"]
            shape.friction = poly["friction"]

            self.shapes.append(shape)

        self.space.add(self.body, *self.shapes)

        #
        self.explosion = Decoration.DynamicDecoration(
            "assets/Spaceships/Default/explosions",
            0.6,
            self.body.position,
            50,
            "explosion")

        self.bullets = []
        self.bullet_offsets = [pygame.math.Vector2(
            50, 50), pygame.math.Vector2(-50, 50)]
        self.dists_to_bullet = [[dist([0, 0], self.bullet_offsets[0]), atan2(self.bullet_offsets[0][0], self.bullet_offsets[0][1])], [dist(
            [0, 0], self.bullet_offsets[1]), atan2(self.bullet_offsets[1][0], self.bullet_offsets[1][1])]]

    def update(self):

        if self.main_engine_on:
            self.body.force = (cos(self.body.angle)*self.engine["forward_acceleration"],
                               sin(self.body.angle)*self.engine["forward_acceleration"])
        if self.side_engine_on == 1:
            self.body.angular_velocity -= self.engine["side_acceleration"]
        elif self.side_engine_on == 2:
            self.body.angular_velocity += self.engine["side_acceleration"]

        self.image = pygame.transform.rotate(
            self.original_image, -1*degrees(self.body.angle)-90)
        self.rect = self.image.get_rect(center=(self.body.position))
        return super().update()

    def shoot(self):

        impulse = (cos(self.body.angle)*self.gun["gun_power"],
                   sin(self.body.angle)*self.gun["gun_power"])

        center_point = self.body.position
        rot_angle = self.body.angle

        bullet_positions = [
            [center_point[0] + cos(rot_angle+rot_offset) * d, center_point[1] + sin(rot_angle+rot_offset) * d] for d, rot_offset in self.dists_to_bullet]

        bullet = Asteroid.Asteroid(self.space,
                                   choice(bullet_positions),
                                   self.gun["bullet_image"],
                                   (self.gun["bullet_r"]*2,
                                    self.gun["bullet_r"]*2),
                                   self.gun["bullet_mass"],
                                   self.gun["bullet_friction"],
                                   self.gun["bullet_elasticity"],
                                   self.gun["bullet_r"]/2)
        bullet.body.apply_impulse_at_local_point(impulse)
        self.groups()[0].add(bullet)

    def destruct(self):

        self.explosion.position = self.body.position
        self.explosion.animating = True
        self.explosion.loops = 1

        self.groups()[0].add(self.explosion)

        num_debris = randint(*self.num_debris)
        for _ in range(num_debris):
            fragment = Asteroid.Asteroid(self.space,
                                         self.body.position,
                                         self.debris_folder_path+"/" +
                                         choice(
                                             listdir(self.debris_folder_path)),
                                         (r:=randint(20,30), r),
                                         5,
                                         0.7,
                                         0.7,
                                         r/2-2)
            fragment.body.velocity = self.body.velocity
            fragment.body.apply_impulse_at_local_point(
                (randint(-10000, 10000), randint(-10000, 10000)))
            self.groups()[0].add(fragment)

        self.groups()[0].remove(self)

        self.space.remove(*self.shapes, self.body)

    def read_from_json(self, file):
        with open(file, "r") as f:
            data = json.load(f)
            self.__dict__ |= data
