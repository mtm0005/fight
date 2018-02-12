# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:39:40 2016

@author: tadmcfall
"""

import pygame

from Color import Color

def message_to_screen(message, display, x_pos, y_pos, size=25,
                       color=Color.black.value,):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    display.blit(text, [x_pos, y_pos])