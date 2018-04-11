#!/usr/bin/env python
import pygame
from math import sqrt
import src.pyignition.PyIgnition
import src.pyignition.particles
import random


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
        self.layer = 0

    def Move(self, x, y):
        """
        Moves the object relative to its current position.
        """
        self.x += x
        self.y += y

    def update(self):
        """
        Updates the object's internals.
        """
        pass

    def draw(self, screen):
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

    def draw(self, screen):
        """
        Do any drawing related to the object.
        """
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.end_x, self.end_y), self.width)


class CircleUnit(BaseUnit):
    """
    Represents a circle drawn on the screen.
    """
    def __init__(self, x=0, y=0, radius=0, width=0, color=None):
        super().__init__(x, y, color)
        self.radius = radius
        self.width = width

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)


class ParticleSpaceUnit(BaseUnit):
    """
    Represents a space where particles are emitted.
    """

    def __init__(self, screen, x=0, y=0, width=0, height=0, color=None):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
        self.is_drawing = False
        self.death = False
        self.death_timer = 50
        self.id = id(self)

        # PyIgnition code for creating a particle effect
        self.effect = src.pyignition.PyIgnition.ParticleEffect(screen, (x, y), (width, height))
        self.source = self.effect.CreateSource(pos=(x, y),
                                               initspeed=0.3,
                                               initdirection=0.0,
                                               initspeedrandrange=0.2,
                                               initdirectionrandrange=3.1415926,
                                               particlesperframe=2,
                                               particlelife=50,
                                               genspacing=1,
                                               drawtype=src.pyignition.PyIgnition.DRAWTYPE_CIRCLE,
                                               colour=color,
                                               radius=2,
                                               length=2,
                                               imagepath=None)

    def draw(self, screen):
        # update and redraw the PyIgnition particle effect
        if self.effect is not None and self.source is not None:
            self.effect.Update()
            self.effect.Redraw()

        if isinstance(self.source, src.pyignition.particles.ParticleSource):
            self.source.Update()

    def update(self):
        if self.death is True:
            if isinstance(self.source, src.pyignition.particles.ParticleSource):
                self.source.emitting = False
            self.death_timer -= 1
            if self.death_timer <= 0:
                self.should_delete = True

    def remove_particles(self):
        self.death = True

    def get_color(self, r, g, b, a):
        """ converts rgba values of 0 - 255 to the equivalent in 0 - 1"""
        return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)


class NoteUnit(BaseUnit):
    """
    This object represents a note in some shape or form.
    Has the ability to fade over time.
    """
    def __init__(self, x=0, y=0, color=None, note=None, fade=False, fade_speed=5, delete_after_fade=False, dissonance=0):
        super().__init__(x, y, color)
        self.note = note
        self.dissonance = dissonance
        self.fade_speed = fade_speed
        self.fade = fade
        self.delete_after_fade = delete_after_fade

    def update(self):
        if self.fade:
            r = self.color[0] - int(self.fade_speed)
            g = self.color[1] - int(self.fade_speed)
            b = self.color[2] - int(self.fade_speed)
            if r < 0:
                r = 0
            if g < 0:
                g = 0
            if b < 0:
                b = 0
            self.color = (r, g, b)

        if self.delete_after_fade:
            if self.color[0] + self.color[1] + self.color[2] == 0:
                self.should_delete = True

    def SetFade(self, toggle=False, speed=5, delete_after=False):
        self.fade_speed = speed
        self.fade = toggle
        self.delete_after_fade = delete_after


class CircleNoteUnit(NoteUnit):
    """
    This object represents a single note as a circle on the screen.
    """
    def __init__(self, x, y, color, note, radius=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

    def update(self):
        pass


class RectNoteUnit(NoteUnit):
    """
    This object represents a single note as a rectangle on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.w = width
        self.h = height

    def draw(self, screen):
        r, g, b = self.color
        r -= self.dissonance * 10
        g -= self.dissonance * 10
        g -= self.dissonance * 10
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        new_color = (r, g, b)
        pygame.draw.rect(screen, new_color, pygame.Rect(self.x, self.y, self.w, self.h))


class AlphaRectNoteUnit(RectNoteUnit):
    """

    """
    def __init__(self, x, y, color, note, width=0, height=0, alpha=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.w = width
        self.h = height
        self.alpha = alpha

    def draw(self, screen):
        r, g, b = self.color
        r -= self.dissonance * 10
        g -= self.dissonance * 10
        g -= self.dissonance * 10
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA | pygame.HWSURFACE)
        s.fill((r, g, b, self.alpha))
        screen.blit(s, (self.x, self.y))


class EllipseNoteUnit(NoteUnit):
    """
    This object represents a single note as an ellipse (stretched out circle) on a screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, line_width=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.w = width
        self.h = height
        self.line_width = line_width

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h), self.line_width)


class DiamondNoteUnit(NoteUnit):
    """
    This object represents a single note as a rhombus.
    """
    def __init__(self, x, y, color, note, radius=0, line_thickness=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.radius = radius
        self.thickness = line_thickness

    def draw(self, screen):
        points = [(self.x, self.y + self.radius + 1),
                  (self.x + self.radius, self.y),
                  (self.x, self.y - self.radius - 1),
                  (self.x - self.radius, self.y)]
        pygame.draw.polygon(screen, self.color, points, self.thickness)


class TriangleNoteUnit(NoteUnit):
    """
    This object represents a single note as a triangle.
    """
    def __init__(self, x, y, color, note, side_length=0, thickness=0, fade=False, fade_speed=5, delete_after_fade=False):
        super().__init__(x, y, color, note, fade, fade_speed, delete_after_fade)
        self.side_length = side_length
        self.thickness = thickness

    def draw(self, screen):
        points = [(self.x, self.y + int((sqrt(3)/3) * self.side_length)),
                  (self.x + int(self.side_length // 2), self.y - int((sqrt(3)/6) * self.side_length)),
                  (self.x - int(self.side_length // 2), self.y - int((sqrt(3)/6) * self.side_length))]
        pygame.draw.polygon(screen, self.color, points, self.thickness)


class RectChordUnit(NoteUnit):
    """
    This object represents a single chord as two thin vertical rectangles on the screen.
    """
    def __init__(self, x, y, color, note, width=0, height=0, sub_width=0):
        super().__init__(x, y, color, note)
        self.w = width
        self.sw = sub_width
        self.h = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.sw, self.h))
        pygame.draw.rect(screen, self.color, pygame.Rect((self.x + self.w) - self.sw, self.y, self.sw, self.h))
