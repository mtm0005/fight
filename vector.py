# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:14:35 2016

@author: tadmcfall
"""

class Vector():

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def print_self(self):
        print('self.x: %f' % self.x)
        print('self.y: %f' % self.y)

    @staticmethod
    def add_vectors(v1, v2):
        resultant_vector = Vector()
        resultant_vector.x = v1.x + v2.x
        resultant_vector.y = v1.y + v2.y
        return resultant_vector

    @staticmethod
    def scalar_multiplication(vector, scalar):
        resultant_vector = Vector()
        resultant_vector.x = vector.x * scalar
        resultant_vector.y = vector.y * scalar
        return resultant_vector
