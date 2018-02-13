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
        self.color = [0, 50, 200]
        self.fade = False
        self.delete_after_fade = False
        self.should_delete = False

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

    def update(self):
        if self.fade:
            self.color[0] -= 2
            self.color[1] -= 2
            self.color[2] -= 2
            if self.color[0] < 0:
                self.color[0] = 0
            if self.color[1] < 0:
                self.color[1] = 0
            if self.color[2] < 0:
                self.color[2] = 0

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


