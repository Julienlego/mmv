#!/usr/bin/env python
import pygame


class BaseUnit:
    """
    This is the base representation of a graphical object in a visualization preset.
    """
    def __init__(self, x, y, note):
        self.x = x
        self.y = y
        self.note = note
        self.color = [0, 50, 200]

    def Move(self, x, y):
        """

        """
        pass

    def Update(self):
        """

        """
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))



class NoteRect(BaseUnit):
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
        self.fade_speed = 5
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
            self.color[0] -= self.fade_speed
            self.color[1] -= self.fade_speed
            self.color[2] -= self.fade_speed
            if self.color[0] < 0:
                self.color[0] = 0
            if self.color[1] < 0:
                self.color[1] = 0
            if self.color[2] < 0:
                self.color[2] = 0

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True
