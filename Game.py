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

path = r""


class Game():

    def __init__(self, config_file, debug=False):

        pygame.init()
        pygame.font.init()

        self.debug = debug
        self.running = True

        self.config_file = config_file
        self.read_config(self.config_file)

        self.window_caption = self.WINDOW["caption"]
        self.window_icon = pygame.image.load(path + self.WINDOW["icon"])
        self.window_width, self.window_height = self.WINDOW["width"], self.WINDOW["height"]
        self.MAX_FPS = self.GAME["max_fps"]
        self.pymunk_physics_calculating_speed_step = self.GAME[
            "pymunk_physics_calculating_speed_step"]
        self.dt = self.pymunk_physics_calculating_speed_step / self.MAX_FPS
        self.num_decorations = self.GAME["num_decorations"]
        self.num_asteroids = self.GAME["num_asteroids"]
        self.area_size_width = self.GAME["area_size_width"]
        self.area_size_height = self.GAME["area_size_height"]

        # pygame

        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.window_caption)
        pygame.display.set_icon(self.window_icon)
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE)

        # pymunk

        self.space = pymunk.Space()
        self.space.gravity = (
            self.GAME["default_gravity_x"], self.GAME["default_gravity_y"])
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
        self.main_group = MainGroup(self.COLORS["default_bg"],
                                    *self.decorations,
                                    self.spaceship,
                                    *self.asteroids,
                                    self.planet)

    def read_config(self, filename):

        self.config = ConfigParser()
        self.config.read(filename)
        self.__dict__ |= {section: {} for section in self.config.sections()}

        for section in self.config.sections():
            for item in self.config.items(section):

                if item[1].isdigit():
                    self.__dict__[section] |= {item[0]: int(item[1])}

                elif item[1].replace('.', '', 1).isdigit():
                    self.__dict__[section] |= {item[0]: float(item[1])}

                else:
                    self.__dict__[section] |= {item[0]: item[1]}

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
            self.clock.tick(self.MAX_FPS)

            controller.read_and_apply_input(self)


if __name__ == '__main__':

    game = Game(debug=0, config_file=path+"config.cfg")
    game.run()
