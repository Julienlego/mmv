#!/usr/bin/env python
import pygame
import music21
import src.Utilities as util


class BasePreset:
    """
    This class is represents the basic preset class object that all
    presets inherit from. None of the methods are actually implemented in this class.

    """

    def __init__(self, viz_manager, name="", desc="A description goes here."):
        # Name of preset. Also used as the key for the preset in the dict.
        self.name = name
        # Description of the visualization preset.
        self.desc = desc
        self.viz_manager = viz_manager

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


class JustTextPreset(BasePreset):
    """

    """
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


class SimpleCirclePreset(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determined by velocity

    """

    def OnFirstLoad(self, score):
        pass

    def PerMessage(self, screen, message):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

        if isinstance(message, music21.note.Note):
            c = util.NoteToColor(message)
            color = (c[0], c[1], c[2])
            radius = 75
            y = int(screen_y / message.octave)
            pos = (int(screen_x / 2), y)

            pygame.draw.circle(screen, color, pos, radius)


class PianoRollPreset(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """

    def OnFirstLoad(self, score):
        pass

    def PerMessage(self, screen, message):
        pass


class StaticPianoRollPreset(BasePreset):
    """
    This is a static preset that graphs the entire song onto the screen in a piano roll fashion.
    This preset is good for looking at the whole song as a whole.
    """

    def OnFirstLoad(self, score):

        # graph each note on the screen based off of pitch, offset, and length
        self.viz_manager.screen.fill((0, 0, 0))
        notes = []
        for notea in score.flat.notes:
            if isinstance(notea, music21.note.Note):
                notes.append(notea)

        print(notes)
        print(len(score.flat.notes))
        for note in notes:
            if isinstance(note, music21.note.Note):
                screen_x = self.viz_manager.main_frame.display.size.x
                screen_y = self.viz_manager.main_frame.display.size.y
                rect = self.viz_manager.GraphNoteRect(score, note, pygame.Rect(0, 0, screen_x, screen_y - 20))
                print(rect)
                pygame.draw.rect(self.viz_manager.screen, (0, 50, 150), rect)

    def PerMessage(self, screen, message):
        pass
