# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:41:18 2016

@author: tadmcfall
"""

import abc
import copy
import math

from vector import Vector

GRAVITY = Vector(0.0, -300.0)

class PhysicsObject(metaclass=abc.ABCMeta):

    def __init__(self, name, mass=1.0, velocity=Vector(), position=Vector()):
        self.name = name
        self.mass = mass
        self.acceleration = Vector()
        self.velocity = velocity
        self.position = position
        self.dt = 0.033

        self.movable = True
        self.can_be_moved_through = True
        self.bounding_shapes = []
        self.falling = True
        self.acceleration_cap = 100000

    @abc.abstractmethod
    def update(self):
        # apply gravity
        self.apply_acceleration(GRAVITY)

        # apply friction
        self._apply_universal_friction()

        # draw updates
        self.draw()

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def colliding_with_object(self, physics_object):
        pass

    def _apply_universal_friction(self):
        # This is to apply a slight friction to all objects in the
        # opposite direction that they are traveling so they don't fly
        # off from one little hit.

        x_axis_friction = 0.0
        if self.velocity.x != 0.0:
            x_axis_friction = (-1) * math.copysign(20, self.velocity.x)

        friction = Vector(x=x_axis_friction)
        self.apply_force(friction)

    def apply_force(self, force):
        # Force is a vector so it should have two componets, x and y.
        acceleration = self.calculate_acceleration(force)
        self.apply_acceleration(acceleration)

    def apply_acceleration(self, acceleration_to_apply):
        # Acceleration is a vector so it should have two componets, x
        # and y.

        # Reverse the y component of the acceleration since the display
        # coordinates are backwards, i.e. point (0, 0) is located at
        # the top left corner of our display.
        acceleration = copy.copy(acceleration_to_apply)
        acceleration.y = (-1) * acceleration.y

        # Add the additional acceleration to our current acceleration.
        acceleration = Vector.add_vectors(acceleration, self.acceleration)

        # Set our current acceleration to the one we just calculated.
        self.acceleration = acceleration

        # Get an updated velocity.
        velocity = self.calculate_velocity(acceleration)
        self.velocity = velocity

        # Get an updated posistion and apply it to our character.
        position = self.calculate_position(velocity)
        self.update_position(position)

    def update_position(self, delta_position):
        self.position.x = self.position.x + delta_position.x
        self.position.y = self.position.y + delta_position.y

    def calculate_acceleration(self, force):
        # F = ma
        acceleration = Vector()
        acceleration.x = force.x/self.mass
        acceleration.y = force.y/self.mass
        return acceleration

    def calculate_velocity(self, acceleration):
        # Integral of acceleration
        # (current_time * acceleration) - (initial_time * acceleration)
        # acceleration * (current_time - initial_time)
        velocity = Vector()
        velocity.x = acceleration.x * self.dt
        velocity.y = acceleration.y * self.dt
        return velocity

    def calculate_position(self, velocity):
        # Integral of velocity
        position = Vector()
        position.x = velocity.x * self.dt
        position.y = velocity.y * self.dt
        return position

    def print_info(self):
        print('---- %s ----' % self.name)
        print('pos.x: %.2f' % self.position.x)
        print('pos.y: %.2f' % self.position.y)