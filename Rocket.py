# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 20:07:27 2016

@author: tadmcfall
"""

import pygame

from BoundingShape import BoundingShape
from Color import Color
from Character import Character
from Physics import PhysicsObject
from vector import Vector

class Rocket(PhysicsObject):

    def __init__(self, display, velocity, position, collision_manager):
        PhysicsObject.__init__(self, 'rocket', mass=1, velocity=velocity,
                               position=position)

        self.display = display
        self.width = 35
        self.height = 10
        self.power = 100
        self.initial_velocity = velocity

        self.bounding_shapes.append(
            BoundingShape([self.position.x, self.position.y,
                           self.width, self.height]))
        self.collision_manager = collision_manager
        if collision_manager:
            self.collision_manager.add_object(self)

        # Variables used to manage explosions.
        self.time_limit = 45
        self.explosion_radius = self.height
        self.exploding = False
        self.exploded = False
        self.items_hit = []

        # This is used to limit how long our explosion lasts.
        self.explosion_counter = 11

    def update(self):
        # Slightly counter gravity
        self.apply_acceleration(Vector(0, 290))

        # Our rocket is burning fuel so it's accelerating.
        if not self.exploding:
            self.apply_force(Vector(self.initial_velocity.x/self.dt, 0))

        self.bounding_shapes[0].rect = [self.position.x, self.position.y,
                                        self.width, self.height]

        # Cap acceleration.
        self.acceleration_cap = 1700
        if self.acceleration.x > self.acceleration_cap:
            self.acceleration.x = self.acceleration_cap
        elif self.acceleration.x < -self.acceleration_cap:
            self.acceleration.x = -self.acceleration_cap

        PhysicsObject.update(self)

    def draw(self):
        if not self.exploding:
            self.draw_rocket()
            if self.time_limit <= 0:
                self.exploding = True
            else:
                self.time_limit -= 1
        else:
            self.draw_explosion()

    def draw_rocket(self):
        # Draw the body of the rocket.
        pygame.draw.rect(self.display, Color.black.value,
                         [self.position.x, self.position.y,
                          self.width, self.height])

        # Draw the nose of the rocket.
        if self.initial_velocity.x > 0:
            pygame.draw.circle(self.display, Color.black.value,
                               [int(self.position.x + self.width),
                                int(self.position.y + self.height/2)],
                               int(self.height/2))
        else:
            pygame.draw.circle(self.display, Color.black.value,
                               [int(self.position.x),
                                int(self.position.y + self.height/2)],
                               int(self.height/2))

        # Draw the exhaust.
        if self.initial_velocity.x > 0:
            points = [(self.position.x, self.position.y),
                      (self.position.x - 10, self.position.y + 5),
                      (self.position.x, self.position.y + 10)]
            pygame.draw.polygon(self.display, Color.red.value, points)
        else:
            points = [(self.position.x + self.width, self.position.y),
                      (self.position.x + self.width + 10, self.position.y + 5),
                      (self.position.x + self.width, self.position.y + 10)]
            pygame.draw.polygon(self.display, Color.red.value, points)

    def draw_explosion(self):
        if self.explosion_counter > 0:
            pygame.draw.circle(self.display, Color.red.value,
                               [int(self.position.x + self.width/2),
                                int(self.position.y + self.height/2)],
                               int(self.explosion_radius))

            self.explosion_radius += self.height/2.5
            self.explosion_counter -= 1

            # Override our existing bounding box.
            self.bounding_shapes[0].rect = [
                self.position.x - self.explosion_radius/2,
                self.position.y - self.explosion_radius + 10,
                2 * self.explosion_radius,
                2 * self.explosion_radius - 10]

            # Uncomment the next line to view the bounding box.
            #pygame.draw.rect(self.display, Color.black.value, self.rect)
        else:
            self.exploded = True
            if self.collision_manager:
                self.collision_manager.remove_object(self)

    def colliding_with_object(self, physics_object):
        if not physics_object.can_be_moved_through:
            self.position.y = physics_object.rect[1] - self.height

        elif isinstance(physics_object, Character):
            sign = -1
            if self.initial_velocity.x > 0:
                sign = 1

            x_force = self.mass * (self.power * physics_object.hit_points) + self.power
            y_force = self.mass * (self.power * physics_object.hit_points) + self.power

            force = Vector(x_force, y_force)
            force = Vector.scalar_multiplication(force, sign)

            if physics_object in self.items_hit:
                force = Vector.scalar_multiplication(force, 0.1)
                physics_object.apply_force(force)
                physics_object.hit_points += 1
            else:
                physics_object.apply_force(force)
                physics_object.hit_points += 10
                self.items_hit.append(physics_object)

            physics_object.taking_damage = True

        self.exploding = True
