#!/usr/bin/env python
import pygame


class BaseUnit:
    """
    This is the base representation of a graphical object in a visualization preset. This could be a line, a shaded box,
    or something that represents a note being played.

    Some objects are just wrappers for pygame.draw functions that are used in a preset.
    Some objects represent a note as some sort of shape (e.x a colored rectangle).

    Every object/unit MUST be added to vizmanager so it can actually be drawn on the pygame screen.
    """
    def __init__(self, x=0, y=0, color=None):
        self.x = x
        self.y = y
        self.color = color
        self.should_delete = False
        self.id = None

    def Move(self, x, y):
        """
        Moves the object relative to its current position.
        """
        self.x += x
        self.y += y

    def Update(self):
        """
        Updates the object's internals.
        """
        pass

    def Draw(self, screen):
        """
        Do any drawing related to the object.
        """
        pass


class LineUnit(BaseUnit):
    """
    This object represents a line drawn on the screen.
    """
    def __init__(self, x=0, y=0, end_x=0, end_y=0, color=None, width=1):
        super().__init__(x, y, color)
        self.end_x = end_x
        self.end_y = end_y
        self.width = width

    def Draw(self, screen):
        """
        Do any drawing related to the object.
        """
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.end_x, self.end_y), self.width)


class NoteUnit(BaseUnit):
    """
    This object represents a note in some shape or form.
    """
    def __init__(self, x=0, y=0, color=None, note=None):
        super().__init__(x, y, color)
        self.note = note


class CircleNoteUnit(NoteUnit):
    """
    This object represents a single note as a circle on the screen.
    """
    def __init__(self, x, y, color, note, radius=0):
        super().__init__(x, y, color, note)
        self.radius = radius
        self.fade = False
        self.fade_speed = 5
        self.delete_after_fade = False

    def Update(self):
        if self.fade:
            self.color[0] -= int(self.fade_speed)
            self.color[1] -= int(self.fade_speed)
            self.color[2] -= int(self.fade_speed)
            if self.color[0] < 0:
                self.color[0] = 0
            if self.color[1] < 0:
                self.color[1] = 0
            if self.color[2] < 0:
                self.color[2] = 0

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True

    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class RectNoteUnit(NoteUnit):
    """
    This object represents a single note as a rectangle on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0):
        super().__init__(x, y, color, note)
        self.w = width
        self.h = height
        self.fade = False
        self.fade_speed = 5
        self.delete_after_fade = False

    def Update(self):
        if self.fade:
            self.color[0] -= int(self.fade_speed)
            self.color[1] -= int(self.fade_speed)
            self.color[2] -= int(self.fade_speed)
            if self.color[0] < 0:
                self.color[0] = 0
            if self.color[1] < 0:
                self.color[1] = 0
            if self.color[2] < 0:
                self.color[2] = 0

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True

    def Draw(self, screen):
        # print("Note color: {0}".format(self.color))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


class ChordUnit(NoteUnit):
    """
    This object represents a single chord as two thin vertical rectangles on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, full_width=0):
        super().__init__(x, y, color, note)
        self.w = width
        self.fw = full_width
        self.h = height
        self.fade = False
        self.fade_speed = 5
        self.delete_after_fade = False

    def Update(self):
        if self.fade:
            self.color[0] -= int(self.fade_speed)
            self.color[1] -= int(self.fade_speed)
            self.color[2] -= int(self.fade_speed)
            if self.color[0] < 0:
                self.color[0] = 0
            if self.color[1] < 0:
                self.color[1] = 0
            if self.color[2] < 0:
                self.color[2] = 0

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True

    def Draw(self, screen):
        # print("Note color: {0}".format(self.color))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color, pygame.Rect((self.x + self.fw) - self.w, self.y, self.w, self.h))
