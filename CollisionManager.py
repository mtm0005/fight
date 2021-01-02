# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 21:55:06 2016

@author: tadmcfall
"""

class CollisionManager():

    def __init__(self, list_of_objects=None, debug=False):

        self.list_of_objects = []
        if list_of_objects is not None:
            self.list_of_objects = list_of_objects
        self.index = 0
        self.debug = debug

    def print_items(self):
        for item in self.list_of_objects:
            print(item.name)

    def add_object(self, physics_object):
        if self.debug:
            print()
            print('----------------------------------------------')
            print('adding object: %s' % physics_object.name)
            self.print_items()

        self.list_of_objects.append(physics_object)

        if self.debug:
            print('item added...')
            self.print_items()
            print('----------------------------------------------')

    def remove_object(self, physics_object):
        if self.debug:
            print()
            print('----------------------------------------------')
            print('removing object: %s' % physics_object.name)
            self.print_items()

        if physics_object in self.list_of_objects:
            self.list_of_objects.remove(physics_object)

        if self.debug:
            print('item removed...')
            self.print_items()
            print('----------------------------------------------')

    def shapes_colliding(self, shape_1, shape_2):
        # Rect is a list containing the coordinates of the upper left
        # hand corner of the Shape's bounding box as the first two
        # items (x then y) and the width and height as the next two
        # items.

        shapes_are_colliding = False
        shapes_are_colliding_y = False
        shapes_are_colliding_x = False

        shape_1_lowest_y = shape_1.rect[1] + shape_1.rect[3]
        shape_1_highest_y = shape_1.rect[1]

        shape_2_lowest_y = shape_2.rect[1] + shape_2.rect[3]
        shape_2_highest_y = shape_2.rect[1]

        if (shape_1_lowest_y >= shape_2_highest_y and
                shape_1_highest_y <= shape_2_lowest_y):
            shapes_are_colliding_y = True

        shape_1_lowest_x = shape_1.rect[0] + shape_1.rect[2]
        shape_1_highest_x = shape_1.rect[0]

        shape_2_lowest_x = shape_2.rect[0] + shape_2.rect[2]
        shape_2_highest_x = shape_2.rect[0]

        if (shape_1_lowest_x >= shape_2_highest_x and
                shape_1_highest_x <= shape_2_lowest_x):
            shapes_are_colliding_x = True

        if (shapes_are_colliding_y and shapes_are_colliding_x):
            shapes_are_colliding = True

        return shapes_are_colliding

    def objects_colliding(self, object_1, object_2):
        for obj1_shape in object_1.bounding_shapes:
            for obj2_shape in object_2.bounding_shapes:
                if self.shapes_colliding(obj1_shape, obj2_shape):
                    return True

        return False

    def update_objects(self):
        current_object = None

        for i in range(len(self.list_of_objects) - 1):
            current_object = self.list_of_objects[i]
            for j in range(i + 1, len(self.list_of_objects)):
                next_object = self.list_of_objects[j]
                if self.objects_colliding(current_object, next_object):
                    current_object.colliding_with_object(next_object)
                    next_object.colliding_with_object(current_object)
