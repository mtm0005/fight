# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:45:13 2016

@author: tadmcfall
"""

import pygame

from Color import Color

class Display():

    def __init__(self, width, height, caption=''):
        self.width = width
        self.height = height
        self.caption = caption

        self.display = pygame.display.set_mode((width, height))
        self.set_caption(caption)

    def set_caption(self, caption):
        self.caption = caption
        pygame.display.set_caption(caption)

    def fill(self, color_value):
        self.display.fill(color_value)

    def display_message(self, message, size=25, color=Color.black.value,
                        x_pos=None, y_pos=None):
        if x_pos is None:
            x_pos = self.width/2

        if y_pos is None:
            y_pos = self.height/2

        font = pygame.font.SysFont(None, size)
        text = font.render(message, True, color)
        self.display.blit(text, [x_pos, y_pos])

    def blit(self, *args, **kwargs):
        self.display.blit(*args, **kwargs)