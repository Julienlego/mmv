#!/usr/bin/env python
import pygame

class BasePreset:
    """
    This class is represents the basic preset class object that all
    presets inherit from. None of the methods are actually implemented in this class.

    """

    def __init__(self, name="", description=""):
        self.name = name
        self.description = description

    def OnFirstLoad(self, score):
        """
        Runs once to gather and store any information relative to the
        song before each frame of the visualization is made.

        YOUR CODE GOES BELOW
        """
        pass

    def PerMessage(self, screen, message):
        """
        Draws given message.

        YOUR CODE GOES BELOW
        """
        pass


class BasicPreset(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determind by velocity

    """

    def OnFirstLoad(self, score):
        pass

    def PerMessage(self, screen, message):
        pygame.draw.circle(screen, (0, 255, 0), (250, 250), 125)
