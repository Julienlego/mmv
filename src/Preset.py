#!/usr/bin/env python
import src.MidiBlock
import pyglet

class BasePreset:
    """
    This class is represents the basic preset class object that all
    presets inherit from. None of the methods are actually implemented in this class.

    """

    def __init__(self):
        self.on_first_load(self)


    def on_first_load(self):
        """
        Runs once to gather and store any information relative to the
        song before each frame of the visualization is made.

        YOUR CODE GOES BELOW
        """
        pass

    def per_message(self, message):
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

    def on_first_load(self):
        pass

    def per_message(self, message):
        pass

    def draw_circle(self, xpos, ypos, radius, color):
        pass
