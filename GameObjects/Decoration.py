import pygame
from os import listdir


class StaticDecoration(pygame.sprite.Sprite):
    def __init__(self, img_path, pos, angle, size="default") -> None:

        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()
        self.position = pos
        self.angle = angle
        self.size = size

        # pygame

        self.image = pygame.transform.rotate(self.image, self.angle)
        if size != "default":
            self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def update(self) -> None:
        return super().update()


class DynamicDecoration(pygame.sprite.Sprite):
    def __init__(self, frames_path, animation_speed, pos, angle, default_frame_name, size="default", loops=float("inf"), atype="standard") -> None:

        super().__init__()

        self.atype = atype
        self.loops = loops
        self.animating = False
        self.position = pos
        self.angle = angle
        self.animation_speed = animation_speed
        self.frames_path = frames_path

        if atype == "standard":
            self.default_frame_name = default_frame_name
            self.size = size
            self.initialize_frames()
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]

        elif atype == "size":
            self.origin_image = pygame.image.load(self.frames_path).convert_alpha()
            self.anim_size = 1
            self.image = pygame.transform.smoothscale(
                self.origin_image, (1, 1))
            self.max_anim_size = self.origin_image.get_size()[0]*2.5

        self.rect = self.image.get_rect(center=self.position)

    def update(self) -> None:

        if self.animating:

            if self.atype == "standard":

                self.cur_frame += self.animation_speed

                if self.cur_frame > len(self.frames):
                    self.cur_frame = 0
                    self.loops -= 1
                    if self.loops == 0:
                        self.groups()[0].remove(self)
                        return

                self.image = self.frames[int(self.cur_frame)]

            elif self.atype == "size":

                if self.anim_size >= self.max_anim_size:
                    self.groups()[0].remove(self)
                    return

                self.image = pygame.transform.smoothscale(self.origin_image, (int(self.anim_size),
                                                                              int(self.anim_size)))
                self.image.set_alpha(255-self.anim_size/5)
                self.anim_size += self.animation_speed * 50

            self.rect = self.image.get_rect(center=self.position)

        return super().update()

    def initialize_frames(self):

        self.frames = []

        for img in sorted(listdir(self.frames_path), key=lambda x: int(x.replace(".png", "").replace(self.default_frame_name, ""))):

            frame = pygame.image.load(self.frames_path+"/"+img).convert_alpha()
            frame = pygame.transform.rotate(frame, self.angle)
            if self.size != "default":
                frame = pygame.transform.smoothscale(frame, self.size)
            self.frames.append(frame)
