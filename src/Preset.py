#!/usr/bin/env python
import pygame
import music21

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
        # get the highest and lowest notes for position normalization
        highest_note = 0
        lowest_note = float("inf")
        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                if note.pitch.midi > highest_note:
                    highest_note = note.pitch.midi
                if note.pitch.midi < lowest_note:
                    lowest_note = note.pitch.midi

        # graph each note on the screen based off of pitch, offset, and length
        self.viz_manager.screen.fill((0, 0, 0))
        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                # print(str(note) + str(note.offset))
                largest_offset = score.flat.notes[len(score.flat.notes) - 1].offset
                number = note.pitch.midi
                x = self.viz_manager.main_frame.display.size.x * float(note.offset / largest_offset)
                y = self.viz_manager.main_frame.display.size.y - (
                ((number - lowest_note) / (highest_note - lowest_note)) * self.viz_manager.main_frame.display.size.y)
                print(str(x) + ", " + str(y))
                pygame.draw.rect(self.viz_manager.screen, (0, 50, 150), (x, y, (
                self.viz_manager.main_frame.display.size.x * float(
                    note.quarterLength / score.flat.notes[len(score.flat.notes) - 1].offset)), 20))

    def PerMessage(self, screen, message):
        pass
