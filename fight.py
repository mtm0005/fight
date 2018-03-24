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

display_width = 1500
display_height = 600
stage_height = 100

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('FIGHT!')

frames_per_second = 30
clock = pygame.time.Clock()

platform = Platform(display)

def draw_stage():
    display.fill(Color.blue.value)
    pygame.draw.rect(display, Color.green.value,
                     [0, display_height - stage_height,
                      display_width, stage_height])
    platform.draw()

def pause_game():
    game_paused = True
    game_over = False
    while game_paused:
        utils.message_to_screen('Game Paused.', display, display_width/2,
                                display_height/2, color=Color.red.value)
        utils.message_to_screen('Press P to play or Q to quit', display,
                          display_width/2, display_height/2+20, color=Color.red.value)
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

    # Set up characters.
    robot_initial_position = Vector(display_width/4,
                                    display_height-stage_height-50)

    cat_initial_position = Vector(display_width - display_width/4 - 55,
                                  display_height-stage_height-50)

    robot = Robot(display, "robot", position=robot_initial_position)
    cat = Cat(display, "cat", is_dummy=False, position=cat_initial_position)
    cat.set_up_key_commands('alt')
    cat.facing_right = False

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
                                    display_width/2, display_height/2)
            utils.message_to_screen('Press P to play or Q to quit', display,
                              display_width/2, display_height/2+20)
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
            for character in characters:
                character.reset()

        # Check for events that don't infulence the game characters
        # movement, e.g. pause or quit events.
        events = copy.copy(pygame.event.get())
        for event in events:
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = pause_game()
                    if game_over:
                        game_reset = True
                    break

        draw_stage()
        collision_manager.update_objects()

        # Update each character in the game.
        for character in characters:
            character.update(events)

            # If the character is going out of the display then the
            # character is dead and needs to be reset.
            # Check the x-axis.
            if character.position.x <= (-character.width + 5):
                character.position.x = -character.width + 5
                character.reset()

            elif character.position.x >= (display_width - 5):
                character.position.x = display_width - 5
                character.reset()

            # Then check the y-axis.
            if character.position.y <= (-character.height + 5):
                character.position.y = -character.height + 5
                character.reset()

            elif character.position.y >= (display_height - 5):
                character.position.y = display_height - 5
                character.reset()

        # Display each characters health
        string_width = 20
        for character in characters:
            health_string = character.name + ': ' + str(character.hit_points)
            utils.message_to_screen(health_string, display, x_pos=string_width,
                                    y_pos=5, color=Color.red.value)
            string_width = string_width + (len(health_string) * 10) + 10

        pygame.display.update()
        clock.tick(frames_per_second)

    pygame.quit()
    quit()

game_loop()