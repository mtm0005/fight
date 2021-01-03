# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:11:57 2016

@author: tadmcfall
"""

import pygame

from BoundingShape import BoundingShape
from Color import Color
from Physics import PhysicsObject
from vector import Vector

class Platform(PhysicsObject):

    def __init__(self, display, position=Vector(), color=Color.black.value):
        PhysicsObject.__init__(self, "platform", position=position)
        self.display = display
        self.color = color
        self.movable = False
        self.can_be_moved_through = False

        self.rect = [
            275,  # left x position
            575,  # top y position
            950,  # length
            10]   # width
        self.bounding_shapes = [BoundingShape(self.rect)]
        self.acceleration = 0

    def draw(self):
        pygame.draw.rect(self.display, self.color, self.rect)

    def update(self, events):
        pass

    def colliding_with_object(self, physics_object):
        #print("platform is colliding with %s" % physics_object.name)
        physics_object.apply_force(Vector(
            y=(physics_object.acceleration.y*physics_object.mass)))

    def apply_force(self, force):
        pass

    def apply_acceleration(self, acceleration_to_apply):
        pass
