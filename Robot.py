# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:24:18 2016

@author: tadmcfall
"""

import copy
import pygame

from BoundingShape import BoundingShape
from Character import Character
from Color import Color
from Rocket import Rocket
from vector import Vector

class Robot(Character):

    def __init__(self, display, name, mass=1.75, position=Vector(),
                 is_dummy=False, *args, **kwargs):

        Character.__init__(self, display, name, is_dummy=is_dummy, mass=mass,
                           position=copy.copy(position), *args, **kwargs)
        self.width = 60
        self.height = 100
        self.bounding_shapes[0] = BoundingShape([self.position.x,
                                                 self.position.y,
                                                 self.width,
                                                 self.height])

        self.attacks = []
        self.manager = None

    def move_left(self):
        self.apply_force(Vector(x=-100, y=0))

    def move_right(self):
        self.apply_force(Vector(x=100, y=0))

    def jump(self):
        self.apply_force(Vector(x=0, y=7500))

    def dodge(self):
        print('dodge')

    def basic_attack(self):
        print('basic attack')

    def special_attack(self):
        print('special attack')

        x_velocity = self.velocity.x
        x_position = 0
        if self.facing_right:
            x_velocity += 120
            x_position = self.position.x + self.width
        else:
            x_velocity -= 120
            # The width of the rocket is 35
            x_position = self.position.x - 35

        velocity = Vector(x_velocity, self.velocity.y)
        position = Vector(x_position, self.position.y + (self.height/2))
        rocket = Rocket(self.display, velocity, position, self.manager)
        self.attacks.append(rocket)

    def update(self, events):
        # Call parent class update.
        Character.update(self, events)

    def draw(self):
        # Draw bounding box
        #pygame.draw.rect(self.display, Color.white.value,
        #                 [self.position.x, self.position.y,
        #                  self.width, self.height])

        # Draw the robot's head
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + self.width/4, self.position.y,
                          self.width/2, self.width/2])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + self.width/4, self.position.y,
                          self.width/2, self.width/2], 3)

        # Draw the eyes
        pygame.draw.circle(self.display, Color.red.value,
                         [int(self.position.x + (3 * self.width)/8),
                          int(self.position.y + self.width/8)], 4)

        pygame.draw.circle(self.display, Color.red.value,
                         [int(self.position.x + (5 * self.width)/8),
                          int(self.position.y + self.width/8)], 4)

        # Draw the mouth
        pygame.draw.rect(self.display, Color.black.value,
                         [int(self.position.x + (3 * self.width)/8),
                          int(self.position.y + (3 * self.width)/8 - 2),
                          self.width/4, 4])

        # Draw the body
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x, self.position.y + self.width/2,
                          self.width, self.width])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x, self.position.y + self.width/2,
                          self.width, self.width], 3)

        # Draw the wheels
        pygame.draw.circle(self.display, Color.black.value,
                           [int(self.position.x + self.width/4),
                           int(self.position.y + (3*self.width)/2 + self.width/12)],
                           int(self.width/12))

        pygame.draw.circle(self.display, Color.black.value,
                           [int(self.position.x + (3*self.width)/4),
                           int(self.position.y + (3*self.width)/2 + self.width/12)],
                           int(self.width/12))

        for attack in self.attacks:
            if not attack.exploded:
                attack.update()
            else:
                self.attacks.remove(attack)
