# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:41:13 2015

@author: tadmcfall
"""

import copy
import pygame
import utils

from Cat import Cat
from CollisionManager import CollisionManager
from Color import Color
from Platform import Platform
from Robot import Robot
from vector import Vector

pygame.init()

NUM_LIVES = 3

DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 600
STAGE_HEIGHT = 100

FRAMES_PER_SECOND = 30

def draw_stage(display, platform):
    display.fill(Color.blue.value)
    pygame.draw.rect(display, Color.green.value,
                     [0, DISPLAY_HEIGHT - STAGE_HEIGHT,
                      DISPLAY_WIDTH, STAGE_HEIGHT])
    platform.draw()

def pause_game(display):
    game_paused = True
    game_over = False
    while game_paused:
        utils.message_to_screen('Game Paused.', display, DISPLAY_WIDTH/2,
                                DISPLAY_HEIGHT/2, color=Color.red.value)
        utils.message_to_screen('Press P to play or Q to quit', display,
                                DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+20,
                                color=Color.red.value)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_paused = False
                    game_over = True
                elif event.key == pygame.K_p:
                    game_paused = False

    return game_over

def game_loop():
    game_exit = False
    game_over = True
    game_reset = True

    cat_won = False
    robot_won = False

    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('FIGHT!')

    clock = pygame.time.Clock()
    platform = Platform(display)

    # Set up characters.
    robot_initial_position = Vector(DISPLAY_WIDTH/4,
                                    DISPLAY_HEIGHT-STAGE_HEIGHT-50)

    cat_initial_position = Vector(DISPLAY_WIDTH - DISPLAY_WIDTH/4 - 55,
                                  DISPLAY_HEIGHT-STAGE_HEIGHT-50)

    robot = Robot(display, "robot", position=robot_initial_position)
    cat = Cat(display, "cat", is_dummy=False, position=cat_initial_position, facing_right=False)
    cat.set_up_key_commands('alt')

    characters = [robot, cat]

    # Set up a CollisionManager with all of our characters and
    # platforms.
    collision_manager = CollisionManager([platform, robot, cat])

    robot.manager = collision_manager
    cat.manager = collision_manager

    collision_manager.print_items()

    while not game_exit:

        # Display main menu until the user starts a game or exits the
        # program.
        while game_over:
            display.fill(Color.white.value)
            utils.message_to_screen('Welcome to Fight!', display,
                                    DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
            utils.message_to_screen('Press P to play or Q to quit', display,
                                    DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+20)
            if cat_won:
                utils.message_to_screen("Cat won!", display,
                                        DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+40)
            elif robot_won:
                utils.message_to_screen("Robot won!", display,
                                        DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+40)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_p:
                        game_over = False

        # Reset our characters if the game is starting over or just
        # began.
        if game_reset:
            game_reset = False
            cat_won = False
            robot_won = False
            for character in characters:
                character.reset()
                character.deaths = 0

        # Check for events that don't infulence the game characters
        # movement, e.g. pause or quit events.
        events = copy.copy(pygame.event.get())
        for event in events:
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = pause_game(display)
                    if game_over:
                        game_reset = True
                    break

        draw_stage(display, platform)
        collision_manager.update_objects()

        # Update each character in the game.
        for character in characters:
            character.update(events)

            # If the character is going out of the display then the
            # character is dead.
            # Check the x-axis.
            if character.position.x <= (-character.width + 5):
                character.position.x = -character.width + 5
                character.die()

            elif character.position.x >= (DISPLAY_WIDTH - 5):
                character.position.x = DISPLAY_WIDTH - 5
                character.die()

            # Then check the y-axis.
            if character.position.y <= (-character.height + 5):
                character.position.y = -character.height + 5
                character.die()

            elif character.position.y >= (DISPLAY_HEIGHT - 5):
                character.position.y = DISPLAY_HEIGHT - 5
                character.die()

            if character.deaths >= NUM_LIVES:
                if character.name == 'robot':
                    cat_won = True
                    robot_won = False
                else:
                    robot_won = True
                    cat_won = False

                # Return to the title screen.
                game_over = True
                game_reset = True

        # Display each characters health
        string_width = 20
        for character in characters:
            health_string = character.name + ': ' + str(character.hit_points)
            utils.message_to_screen(health_string, display, x_pos=string_width,
                                    y_pos=5, color=Color.red.value)
            utils.message_to_screen('{}'.format(NUM_LIVES-character.deaths),
                                    display, x_pos=string_width, y_pos=25,
                                    color=Color.red.value)
            string_width = string_width + (len(health_string) * 10) + 10

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()
    quit()

game_loop()
