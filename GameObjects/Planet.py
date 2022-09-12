import pygame
import pymunk
from dataclasses import dataclass
from math import degrees, dist, atan2, cos, sin


@dataclass(eq=False)
class Planet(pygame.sprite.Sprite):
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

        self.gravity_radius = self.radius*12
        self.gravity_constant = 4*10**5

        # pymunk init
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
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
        self.image = pygame.transform.rotate(
            self.original_image, degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.position)

    def update(self) -> None:

        for body in self.space.bodies:

            if body == self.body:
                continue

            # Gravity

            if dist(self.body.position, body.position) < self.gravity_radius:

                gravity_force = self.calculate_gravity_to(body)
                angle = atan2(self.body.position[1]-body.position[1],
                              self.body.position[0]-body.position[0])
                x_projection = cos(angle) * gravity_force
                y_projection = sin(angle) * gravity_force

                old_x_force = body.force[0]
                old_y_force = body.force[1]

                body.force = (old_x_force+x_projection,
                              old_y_force+y_projection)

        return super().update()

    def calculate_gravity_to(self, body):
        force = self.gravity_constant * \
            (self.mass*body.mass)/dist(self.body.position, body.position)**2
        return force
