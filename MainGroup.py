import pygame


class MainGroup(pygame.sprite.Group):
    def __init__(self, bg_color, *sprites) -> None:

        super().__init__(*sprites)
        self.display_surface = pygame.display.get_surface()
        self.bg_color = bg_color

        # camera offset
        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # zoom
        self.zoom_scale = 1
        self.max_zoom = 1.5
        self.internal_surf_size = (
            self.max_zoom*self.display_surface.get_size()[0],
            self.max_zoom*self.display_surface.get_size()[1])
        self.internal_surf = pygame.Surface(
            self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surf_size)

    def on_resize(self):
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.internal_surf_size = (
            self.max_zoom*self.display_surface.get_size()[0],
            self.max_zoom*self.display_surface.get_size()[1])
        self.internal_surf = pygame.Surface(
            self.internal_surf_size, pygame.SRCALPHA)
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surf_size)

    def draw(self):

        self.display_surface.fill(self.bg_color)
        self.internal_surf.fill(self.bg_color)
        for sprite in self.sprites():
            self.internal_surf.blit(
                sprite.image, sprite.rect.topleft - self.offset)

        scaled_surf = pygame.transform.scale(
            self.internal_surf,
            self.internal_surface_size_vector * self.zoom_scale
        )
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(
            scaled_surf,
            scaled_rect
        )
