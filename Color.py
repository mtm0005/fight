# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:36:52 2015

@author: tadmcfall
"""

from enum import Enum

class Color(Enum):
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 155, 0)
    dark_green = (6, 99, 14)
    blue = (0, 0, 255)
    grey = (173, 173, 173)

    def __init__(self, r_value, g_value, b_value):
        self.r_value = r_value
        self.g_value = g_value
        self.b_value = b_value