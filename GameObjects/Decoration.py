import pygame
from math import degrees


class StaticDecoration(pygame.sprite.Sprite):
    def __init__(self, img_path, pos, angle, size="default") -> None:

        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()
        self.position = pos
        self.angle = angle
        self.size = size

        # pygame

        self.image = pygame.transform.rotate(self.image, degrees(self.angle))
        if size != "default":
            self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def update(self) -> None:
        return super().update()
