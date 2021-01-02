# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:59:29 2015

@author: tadmcfall
"""

import abc
import copy
import pygame

from BoundingShape import BoundingShape
from Physics import PhysicsObject
from vector import Vector

class Character(PhysicsObject, metaclass=abc.ABCMeta):

    def __init__(self, display, name, mass=1.0, position=Vector(), is_dummy=False,
                 facing_right=True, running_acceleration_cap=1400):

        PhysicsObject.__init__(self, name, mass=mass, position=position)
        self.display = display
        self.hit_points = 0
        self.width = 0
        self.height = 0
        self.moving_right = False
        self.moving_left = False
        self.facing_right = facing_right
        self.initially_facing_right = facing_right
        self.dodging = False
        self.bounding_shapes = [BoundingShape([0, 0, 0, 0])]
        self.is_dummy = is_dummy
        self.running_acceleration_cap = running_acceleration_cap
        self.damage_acceleration_cap = 100000
        self.taking_damage = False
        self.jumping = False
        self.double_jumping = False
        self.initial_position = copy.copy(self.position)
        self.is_alive = True
        self.deaths = 0

        self.set_up_key_commands()

    def set_up_key_commands(self, key_set_up='default'):
        if key_set_up == 'default':
            self.move_left_key = pygame.K_a
            self.move_right_key = pygame.K_d
            self.jump_key = pygame.K_w
            self.dodge_key = pygame.K_s
            self.basic_attack_key = pygame.K_q
            self.special_attack_key = pygame.K_e
        else:
            self.move_left_key = pygame.K_j
            self.move_right_key = pygame.K_l
            self.jump_key = pygame.K_i
            self.dodge_key = pygame.K_k
            self.basic_attack_key = pygame.K_u
            self.special_attack_key = pygame.K_o

    def reset(self):
        self.hit_points = 0
        self.acceleration = Vector()
        self.velocity = Vector()
        self.position = copy.copy(self.initial_position)
        self.jumping = False
        self.double_jumping = False
        self.falling = False
        self.taking_damage = False
        self.dodging = False
        self.moving_left = False
        self.moving_right = False
        self.facing_right = self.initially_facing_right

    def die(self):
        self.deaths += 1
        self.reset()

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def update(self, events):
        # Cap acceleration.
        if not self.taking_damage:
            self._apply_acceleration_cap(self.running_acceleration_cap)
        else:
            self._apply_acceleration_cap(self.damage_acceleration_cap)

            if abs(self.acceleration.x) <= self.running_acceleration_cap:
                self.taking_damage = False

        # Don't try to play if you are just a dummy.
        # This is not refering to Ben... or Haleigh.
        if self.is_dummy:
            self._update_position()
            PhysicsObject.update(self)
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.move_left_key:
                    self.moving_left = True
                elif event.key == self.move_right_key:
                    self.moving_right = True
                elif event.key == self.jump_key:
                    self.attempt_jump()
                elif event.key == self.dodge_key:
                    self.dodge()
                elif event.key == self.basic_attack_key:
                    self.basic_attack()
                elif event.key == self.special_attack_key:
                    self.special_attack()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Left click
                    self.basic_attack()
                elif event.button == 3:
                    # Right click
                    self.special_attack()
            elif event.type == pygame.KEYUP:
                if event.key == self.move_left_key:
                    self.moving_left = False
                elif event.key == self.move_right_key:
                    self.moving_right = False

        self._update_position()
        PhysicsObject.update(self)

    def _apply_acceleration_cap(self, acceleration_cap):
        if self.acceleration.x > acceleration_cap:
            self.acceleration.x = acceleration_cap
        elif self.acceleration.x < -acceleration_cap:
            self.acceleration.x = -acceleration_cap

    def _update_position(self):
        if self.moving_right:
            self.facing_right = True
            self.move_right()
        elif self.moving_left:
            self.facing_right = False
            self.move_left()

        self.bounding_shapes[0].rect = [self.position.x, self.position.y,
                                        self.width, self.height]

    def colliding_with_object(self, physics_object):
        # This is a temporary hack. If we collide with an object that
        # we can't move through just lock onto it's top plane.
        if not physics_object.can_be_moved_through:
            self.position.y = physics_object.rect[1] - self.height
            self.jumping = False
            self.double_jumping = False

    @abc.abstractmethod
    def move_left(self):
        pass

    @abc.abstractmethod
    def move_right(self):
        pass

    def attempt_jump(self):

        if ((not self.jumping) or (self.jumping and not self.double_jumping)):
            # Set y acceleration to zero.
            self.acceleration.y = 0
            self.jump()

            if self.jumping:
                self.double_jumping = True
            else:
                self.jumping = True

    @abc.abstractmethod
    def jump(self):
        pass

    @abc.abstractmethod
    def dodge(self):
        pass

    @abc.abstractmethod
    def basic_attack(self):
        pass

    @abc.abstractmethod
    def special_attack(self):
        pass
