# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 14:59:05 2016

@author: tadmcfall
"""

import copy
import pygame

from BoundingShape import BoundingShape
from Character import Character
from Color import Color
from Rocket import Rocket
from vector import Vector

class Cat(Character):

    def __init__(self, display, name, mass=1.0, position=Vector(),
                 is_dummy=False):

        Character.__init__(self, display, name, is_dummy=is_dummy, mass=mass,
                           position=copy.copy(position), running_acceleration_cap=2000)

        self.width = 90
        self.height = 70

        self.bounding_shapes[0] = BoundingShape([self.position.x,
                                                 self.position.y,
                                                 self.width,
                                                 self.height])
    
        self.attacks = []

    def move_left(self):
        self.apply_force(Vector(x=-100, y=0))

    def move_right(self):
        self.apply_force(Vector(x=100, y=0))

    def jump(self):
        self.apply_force(Vector(x=0, y=6500))

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

        if self.facing_right:
            self.draw_facing_right()
        else:
            self.draw_facing_left()

        for attack in self.attacks:
            if not attack.exploded:
                attack.update()
            else:
                self.attacks.remove(attack)

    def draw_facing_left(self):
        # Draw the cat's head
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x, self.position.y,
                          self.width/3, 3 * self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x, self.position.y,
                          self.width/3, 3 * self.height/7], 3)

        # Draw the ear.
        ear_points = [(self.position.x + 2 * self.width/9, self.position.y),
                      (self.position.x + 3 * self.width/9, self.position.y),
                      (self.position.x + 5 * self.width/18,
                       self.position.y - self.height/7)]

        pygame.draw.polygon(self.display, Color.grey.value, ear_points)
        pygame.draw.polygon(self.display, Color.black.value, ear_points, 3)

        # Draw the nose.
        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x - self.width/18,
                          self.position.y + self.height/7,
                          self.width/18, self.height/7])

        # Draw the whiskers.
        start_whiskers_point = (self.position.x + self.width/36,
                                self.position.y + 2 * self.height/7)

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + self.width/9,
                          self.position.y + 3 * self.height/7))

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + 3 * self.width/18,
                          self.position.y + 5 * self.height/14))

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + 5 * self.width/36,
                          self.position.y + 3 * self.height/14))

        # Draw the eye.
        pygame.draw.circle(self.display, Color.dark_green.value,
                         [int(self.position.x + self.width/9),
                          int(self.position.y + self.height/7)],
                          int(self.width/36))

        # Draw the body.
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + 2 * self.width/9,
                          self.position.y + 3 * self.height/7,
                          2 * self.width/3, 3 * self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + 2 * self.width/9,
                          self.position.y + 3 * self.height/7,
                          2 * self.width/3, 3 * self.height/7], 3)

        # Draw the feet.
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + 2 * self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + 2 * self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7], 3)

        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + 7 * self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + 7 * self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7], 3)

        # Draw the tail.
        tail_points = [(self.position.x + 8 * self.width/9, self.position.y + 3 * self.height/7),
                       (self.position.x + 17 * self.width/18, self.position.y),
                       (self.position.x + self.width, self.position.y),
                       (self.position.x + self.width, self.position.y + self.height/18),
                       (self.position.x + 8 * self.width/9, self.position.y + 4 * self.height/7)]

        pygame.draw.polygon(self.display, Color.grey.value, tail_points)
        pygame.draw.polygon(self.display, Color.black.value, tail_points, 3)

    def draw_facing_right(self):
        # Draw the cat's head
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + 2 * self.width/3, self.position.y,
                          self.width/3, 3 * self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + 2 * self.width/3, self.position.y,
                          self.width/3, 3 * self.height/7], 3)

        # Draw the ear.
        ear_points = [(self.position.x + 2 * self.width/3, self.position.y),
                      (self.position.x + 7 * self.width/9, self.position.y),
                      (self.position.x + 13 * self.width/18,
                       self.position.y - self.height/7)]

        pygame.draw.polygon(self.display, Color.grey.value, ear_points)
        pygame.draw.polygon(self.display, Color.black.value, ear_points, 3)

        # Draw the nose.
        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + self.width,
                          self.position.y + self.height/7,
                          self.width/18, self.height/7])

        # Draw the whiskers
        start_whiskers_point = (self.position.x + 35 * self.width/36,
                                self.position.y + 2 * self.height/7)

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + 8 * self.width/9,
                          self.position.y + 3 * self.height/7))

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + 15 * self.width/18,
                          self.position.y + 5 * self.height/14))

        pygame.draw.line(self.display, Color.black.value, start_whiskers_point,
                         (self.position.x + 31 * self.width/36,
                          self.position.y + 3 * self.height/14))

        # Draw the eye.
        pygame.draw.circle(self.display, Color.dark_green.value,
                         [int(self.position.x + 8 * self.width/9),
                          int(self.position.y + self.height/7)],
                          int(self.width/36))

        # Draw the body.
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + self.width/9,
                          self.position.y + 3 * self.height/7,
                          2 * self.width/3, 3 * self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + self.width/9,
                          self.position.y + 3 * self.height/7,
                          2 * self.width/3, 3 * self.height/7], 3)

        # Draw the feet.
        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + self.width/9,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7], 3)

        pygame.draw.rect(self.display, Color.grey.value,
                         [self.position.x + 2 * self.width/3,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7])

        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x + 2 * self.width/3,
                          self.position.y + 6 * self.height/7,
                          self.width/9, self.height/7], 3)

        # Draw the tail.
        tail_points = [(self.position.x + self.width/9, self.position.y + 3 * self.height/7),
                       (self.position.x + self.width/18, self.position.y),
                       (self.position.x, self.position.y),
                       (self.position.x, self.position.y + self.height/18),
                       (self.position.x + self.width/9, self.position.y + 4 * self.height/7)]

        pygame.draw.polygon(self.display, Color.grey.value, tail_points)
        pygame.draw.polygon(self.display, Color.black.value, tail_points, 3)