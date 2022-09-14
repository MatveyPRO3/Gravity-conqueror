import pygame
from random import random


def read_and_apply_input(game):

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()

    # Controlling camera

    if keys[pygame.K_LEFT]:
        game.main_group.offset += (-10, 0)
    if keys[pygame.K_RIGHT]:
        game.main_group.offset += (10, 0)
    if keys[pygame.K_UP]:
        game.main_group.offset += (0, -10)
    if keys[pygame.K_DOWN]:
        game.main_group.offset += (0, 10)

    # Shooting

    if keys[pygame.K_w]:
        if random()>0.7:
            game.spaceship.shoot()

    for event in pygame.event.get():

        # Quitting

        if event.type == pygame.QUIT:
            pygame.quit()
            game.running = False
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game.running = False
            return

        # handling resize

        if event.type == pygame.VIDEORESIZE:
            game.main_group.on_resize()

        # restart

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game.__init__(game.config, debug=game.debug)

        # Controlling main engine

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.spaceship.main_engine_on = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            game.spaceship.main_engine_on = False

        # Controlling side engine

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            game.spaceship.side_engine_on = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            game.spaceship.side_engine_on = 2
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            if game.spaceship.side_engine_on == 2:
                game.spaceship.side_engine_on = False
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            if game.spaceship.side_engine_on == 1:
                game.spaceship.side_engine_on = False

        # zoom

        if event.type == pygame.MOUSEWHEEL:
            if (game.main_group.zoom_scale + event.y * 0.03) > 1/game.main_group.max_zoom and (game.main_group.zoom_scale + event.y * 0.03) < game.main_group.max_zoom:
                game.main_group.zoom_scale += event.y * 0.03

        if event.type == pygame.MOUSEBUTTONUP:
            if game.debug:
                pos = pygame.mouse.get_pos()
                print(list((pos[0]-502, pos[1]-302)), ",")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            game.spaceship.destruct()