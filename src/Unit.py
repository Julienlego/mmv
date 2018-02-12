#!/usr/bin/env python
import music21
import pygame


class NoteRect:
    """
    This class holds information about a graphical object.
    """

    def __init__(self, rect, note):
        self.x = rect.left
        self.y = rect.top
        self.w = rect.width
        self.h = rect.height
        self.rect = rect
        self.color = (0, 50, 200)

        self.note = note

    def move(self, x, y):
        """
        Moves the rect relative to its current position
        :param x: x movement
        :param y: y movement
        :return: none
        """

        self.x += x
        self.y += y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


