import pygame
import pymunk
from configparser import ConfigParser
from GameObjects import Spaceship, Decoration, Asteroid, Planet
import pymunk.pygame_util
from MainGroup import *
import Controller as controller
import random as rand
import os
from math import degrees
from config import *

path = r""


class Game():

    def __init__(self, debug=False):

        pygame.init()
        pygame.font.init()

        self.debug = debug
        self.running = True

        self.__dict__ |= GAME.__dict__
        self.window = WINDOW.__dict__
        self.colors = COLORS.__dict__
        
        self.window_icon = pygame.image.load(path + self.window["icon"])
        self.dt = self.pymunk_physics_calculating_speed_step / self.max_fps

        # pygame
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.window["caption"])
        pygame.display.set_icon(self.window_icon)
        self.screen = pygame.display.set_mode(
            (self.window["width"], self.window["height"]), pygame.RESIZABLE)

        # pymunk

        self.space = pymunk.Space()
        self.space.gravity = (
            self.default_gravity_x, self.default_gravity_y)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # pygame

        # Characteristics text
        self.characteristics_font = pygame.font.SysFont("calibri", 30)

        # "Loading" text
        self.loading_font = pygame.font.SysFont('calibri', 50)
        self.loading_text_surface = self.loading_font.render(
            "Loading...", True, (0, 255, 191))
        self.screen.blit(self.loading_text_surface, (50, 50))
        pygame.display.update()

        # Decorations
        self.decorations = [Decoration.StaticDecoration(
            path+"assets/Decorations/static/"+rand.choice(
                os.listdir(path+"assets/Decorations/static")),
            (rand.randint(0, self.area_size_width),
                rand.randint(0, self.area_size_height)),
            0)
            for _ in range(self.num_decorations)]

        # Player
        self.spaceship = Spaceship.Spaceship(
            self.space, (500, 300),
            path+"assets/Spaceships/Default/default.json")

        # Asteroids
        self.asteroids = [Asteroid.Asteroid(
            self.space,
            (rand.randint(0, self.area_size_width),
                rand.randint(0, self.area_size_height)),
            path + "assets/Asteroids/asteroid.png",
            (asteroid_size := rand.randint(3, 30), asteroid_size),
            1/900 * asteroid_size**2,
            0.7,
            0.7,
            asteroid_size/2)
            for _ in range(self.num_asteroids)]

        # Planets
        self.planet = Planet.Planet(self.space,
                                    (100, -500),
                                    path+"assets/Planets/planet.png",
                                    (590, 590),
                                    100,
                                    0.9,
                                    0.5,
                                    275)

        # Appending all sprites to groups
        self.main_group = MainGroup(self.colors["default_bg"],
                                    self.space,
                                    *self.decorations,
                                    self.spaceship,
                                    *self.asteroids,
                                    self.planet)
        self.spaceship.detect_main_group()

    def draw_text(self):
        text = f"[Pos]: {round(self.spaceship.body.position[0],1)} | {round(self.spaceship.body.position[1],1)}\n[Rot]: {round(degrees(self.spaceship.body.angle),1)}\n[Vel]: {round(self.spaceship.body.velocity[0],1)} | {round(self.spaceship.body.velocity[1],1)}\n[RotVel]: {round(self.spaceship.body.angular_velocity,1)}"
        for i, j in enumerate(text.splitlines()):
            self.screen.blit(self.characteristics_font.render(
                j,
                True, (246, 124, 0)), (500, 30+30*i))

    def draw_all(self):
        self.main_group.update()
        self.main_group.draw()
        self.draw_text()
        if self.debug:
            self.space.debug_draw(self.draw_options)

    def run(self):

        # Main loop

        while self.running:

            self.draw_all()
            self.space.step(self.dt)
            pygame.display.update()
            self.clock.tick(self.max_fps)

            controller.read_and_apply_input(self)


if __name__ == '__main__':

    game = Game(debug=0)
    game.run()
