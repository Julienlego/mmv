#!/usr/bin/env python
import pygame
import math


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
    Has the ability to fade over time.
    """
    def __init__(self, x=0, y=0, color=None, note=None, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color)
        self.note = note
        self.fade = fade
        self.fade_speed = fade_speed
        self.delete_after_fade = delete_after_fade

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


class CircleNoteUnit(NoteUnit):
    """
    This object represents a single note as a circle on the screen.
    """
    def __init__(self, x, y, color, note, radius=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.radius = radius

    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class RectNoteUnit(NoteUnit):
    """
    This object represents a single note as a rectangle on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.w = width
        self.h = height

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))


class EllipseNoteUnit(NoteUnit):
    """
    This object represents a single note as an ellipse (stretched out circle) on a screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, line_width=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.w = width
        self.h = height
        self.line_width = line_width

    def Draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h), self.line_width)


class RhombusNoteUnit(NoteUnit):
    """
    This object represents a single note as a rhombus.
    """
    def __init__(self, x, y, color, note, radius=0, line_thickness=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.radius = radius
        self.thickness = line_thickness

    def Draw(self, screen):
        points = [(self.x - self.radius, self.y), (self.x + self.radius, self.y),
                  (self.x, self.y + self.radius), (self.x, self.y - self.radius)]
        pygame.draw.line(screen, self.color, False, points, self.thickness)


class TriangleNoteUnit(NoteUnit):
    """
    This object represents a single note as a triangle.
    """
    def __init__(self, x, y, color, note, side_length=0, line_thickness=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.side_length = side_length
        self.thickness = line_thickness

    def Draw(self, screen):
        points = [(self.x, self.y + (((math.sqrt(3)/3) * self.side_length) // 1)),
                  (self.x + (self.side_length // 2), self.y - (((math.sqrt(3)/6) * self.side_length) // 1)),
                  (self.x - (self.side_length // 2), self.y - (((math.sqrt(3)/6) * self.side_length) // 1))]
        pygame.draw.line(screen, self.color, False, points, self.thickness)


class RectChordUnit(NoteUnit):
    """
    This object represents a single chord as two thin vertical rectangles on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, sub_width=0):
        super().__init__(x, y, color, note)
        self.w = width
        self.sw = sub_width
        self.h = height

    def Draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.sw, self.h))
        pygame.draw.rect(screen, self.color, pygame.Rect((self.x + self.w) - self.sw, self.y, self.sw, self.h))
