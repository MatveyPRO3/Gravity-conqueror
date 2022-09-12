import pygame
import pymunk
from dataclasses import dataclass
from math import degrees


@dataclass(eq=False)
class Asteroid(pygame.sprite.Sprite):
    space: pymunk.Space
    position: list
    img_path: str
    image_size: tuple
    mass: float
    friction: float
    elasticity: float
    radius: float
    polygons: list = None

    def __post_init__(self) -> None:

        super().__init__()

        # pymunk init
        self.body = pymunk.Body()
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.mass = self.mass
        self.shape.friction = self.friction
        self.shape.elasticity = self.elasticity

        self.space.add(self.body, self.shape)

        # pygame init
        self.original_image = pygame.image.load(self.img_path).convert_alpha()
        self.original_image = pygame.transform.smoothscale(
            self.original_image, self.image_size)
        self.rect = self.original_image.get_rect(center=self.body.position)

    def update(self) -> None:

        self.image = pygame.transform.rotate(
            self.original_image, -1*degrees(self.body.angle)-90)
        self.rect = self.image.get_rect(center=(self.body.position))

        return super().update()
