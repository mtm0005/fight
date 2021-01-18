# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:41:13 2015

@author: tadmcfall
"""

import copy
import pygame
import socket
import sys
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

class Event():

    def __init__(self, key, type_='keydown'):
        self.type = type_
        self.key = key

    def to_bytes(self):
        return f'k: {self.key}, t: {self.type}\n'.encode('utf-8')

def update_characters(characters, events):
    robot_won = False
    cat_won = False
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

    return robot_won, cat_won

def display_lives_and_health(display, characters):
    string_width = 20
    for character in characters:
        health_string = f'{character.name}: {character.hit_points}'
        utils.message_to_screen(health_string, display, x_pos=string_width,
                                y_pos=5, color=Color.red.value, disable_auto_offset=True)
        utils.message_to_screen(f'{NUM_LIVES-character.deaths}',
                                display, x_pos=string_width, y_pos=25,
                                color=Color.red.value, disable_auto_offset=True)
        string_width = string_width + (len(health_string) * 16)

def display_title_screen(display, robot_won=False, cat_won=False, game_paused=False):
    msg = 'Welcome to Fight!'
    color = Color.black.value
    if not game_paused:
        display.fill(Color.white.value)
    else:
        msg = 'Game Paused.'
        color = Color.red.value

    utils.message_to_screen(msg, display, DISPLAY_WIDTH/2,
                            DISPLAY_HEIGHT/2, color=color)
    utils.message_to_screen('Press P to play or Q to quit', display,
                            DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+20, color=color)
    if cat_won:
        utils.message_to_screen("Cat won!", display,
                                DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+40)
    elif robot_won:
        utils.message_to_screen("Robot won!", display,
                                DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2+40)
    pygame.display.update()

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
        display_title_screen(display, game_paused=True)
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


def get_character_data_from_bytes(raw_bytes):
    robot_data = Robot(None, '')
    cat_data = Cat(None, '')

    try:
        robot_str, cat_str, _ = raw_bytes.decode('utf-8').split('\n')
    except Exception as e:
        print(f'Error reading raw_bytes: {raw_bytes}')
        raise e

    for key_value_pair in robot_str.split(','):
        k, v = key_value_pair.split(':')
        k = k.strip()
        v = v.strip()
        if k == 'hp':
            robot_data.hit_points = int(v)
        elif k == 'px':
            robot_data.position.x = float(v)
        elif k == 'py':
            robot_data.position.y = float(v)
        else:
            raise KeyError(f'Invalid key, {k}, found in raw bytes:\n{raw_bytes}')

    for key_value_pair in cat_str.split(','):
        k, v = key_value_pair.split(':')
        k = k.strip()
        v = v.strip()
        if k == 'hp':
            cat_data.hit_points = int(v)
        elif k == 'px':
            cat_data.position.x = float(v)
        elif k == 'py':
            cat_data.position.y = float(v)
        else:
            raise KeyError(f'Invalid key, {k}, found in raw bytes:\n{raw_bytes}')

    return robot_data, cat_data


def convert_events_to_bytes(events):
    for event in events:
        if event.key == pygame.K_w:
            event.key = 'w'
        elif event.key == pygame.K_a:
            event.key = 'a'
        elif event.key == pygame.K_s:
            event.key = 's'
        elif event.key == pygame.K_d:
            event.key = 'd'
        elif event.key == pygame.K_e:
            event.key = 'e'

        elif event.key == pygame.K_i:
            event.key = 'i'
        elif event.key == pygame.K_j:
            event.key = 'j'
        elif event.key == pygame.K_k:
            event.key = 'k'
        elif event.key == pygame.K_l:
            event.key = 'l'
        elif event.key == pygame.K_o:
            event.key = 'o'

    return b''.join([event.to_bytes() for event in events])


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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((sys.argv[1], int(sys.argv[2])))
    print(s.recv(1024)) # Hello from server
    print(s.recv(1024)) # start game

    while not game_exit:

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
        events_to_send = []
        for event in events:
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                events_to_send.append(Event(event.key))
            elif event.type == pygame.KEYUP:
                events_to_send.append(Event(event.key, 'keyup'))
                
        # Send events to server (must be sent as a bytes object)
        bytes_to_send = convert_events_to_bytes(events_to_send)
        if not bytes_to_send:
            s.send('nodata'.encode('utf-8'))
        else:
            s.sendall(bytes_to_send)

        draw_stage(display, platform)
        
        # get data from server
        robot_data, cat_data = get_character_data_from_bytes(s.recv(1024))
        #robot.acceleration = robot_data.acceleration
        #robot.attacks = robot_data.attacks
        #robot.deaths = robot_data.deaths
        #robot.double_jumping = robot_data.double_jumping
        #robot.facing_right = robot_data.facing_right
        #robot.falling = robot_data.falling
        robot.hit_points = robot_data.hit_points
        #robot.is_alive = robot_data.is_alive
        #robot.jumping = robot_data.jumping
        robot.position = robot_data.position
        #robot.taking_damage = robot_data.taking_damage
        #robot.velocity = robot_data.velocity
        
        #cat.acceleration = cat_data.acceleration
        #cat.attacks = cat_data.attacks
        #cat.deaths = cat_data.deaths
        #cat.double_jumping = cat_data.double_jumping
        #cat.facing_right = cat_data.facing_right
        #cat.falling = cat_data.falling
        cat.hit_points = cat_data.hit_points
        #cat.is_alive = cat_data.is_alive
        #cat.jumping = cat_data.jumping
        cat.position = cat_data.position
        #cat.taking_damage = cat_data.taking_damage
        #cat.velocity = cat_data.velocity

        display_lives_and_health(display, characters)
        for c in characters:
            c.draw()

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()
    quit()

game_loop()
