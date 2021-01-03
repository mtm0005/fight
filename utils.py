# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:39:40 2016

@author: tadmcfall
"""

import pygame

from Color import Color

def message_to_screen(message, display, x_pos, y_pos, size=25,
                      color=Color.black.value, disable_auto_offset=False):
    font = pygame.font.SysFont('consolas', size)
    text = font.render(message, True, color)

    # Apply offset to center text unless caller disables this
    # TODO: find a better way to do this. This will only work
    # with this font and my laptop's screen resolution
    if not disable_auto_offset:
        x_pos = x_pos - (len(message) * 7)
        y_pos = y_pos - 9
    display.blit(text, [x_pos, y_pos])
