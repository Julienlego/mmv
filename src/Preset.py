#!/usr/bin/env python
import pygame
import music21
import src.Utilities as util
import src.Unit as Unit
import random


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
        self.lowest_pitch = float("inf")
        self.highest_pitch = 0

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
        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                if note.pitch.midi > self.highest_pitch:
                    self.highest_pitch = note.pitch.midi
                if note.pitch.midi < self.lowest_pitch:
                    self.lowest_pitch = note.pitch.midi
            if isinstance(note, music21.chord.Chord):
                chord_notes = note._notes
                for chord_note in chord_notes:
                    if isinstance(chord_note, music21.note.Note):
                        if chord_note.pitch.midi > self.highest_pitch:
                            self.highest_pitch = chord_note.pitch.midi
                        if chord_note.pitch.midi < self.lowest_pitch:
                            self.lowest_pitch = chord_note.pitch.midi

    def PerMessage(self, screen, note, player):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        rect = pygame.Rect(0, 0, screen_x, screen_y - 20)
        y = self.viz_manager.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, rect)
        new_rect = pygame.Rect(300, y, 200, 20)
        note_rect = Unit.NoteRect(new_rect, note)
        note_rect.fade = True
        note_rect.delete_after_fade = True
        random.seed()
        color = [0, random.randint(50, 100), random.randint(150, 200)]
        note_rect.color = color
        self.viz_manager.units.append(note_rect)
        print(self.viz_manager.units)
        player.note_on(note.pitch.midi, 100)

        # pygame.draw.rect(self.viz_manager.screen, (0, 50, 150), rect)


class StaticPianoRollPreset(BasePreset):
    """
    This is a static preset that graphs the entire song onto the screen in a piano roll fashion.
    This preset is good for looking at the whole song as a whole.
    """

    def OnFirstLoad(self, score):

        # graph each note on the screen based off of pitch, offset, and length
        self.viz_manager.screen.fill((0, 0, 0))
        notes = []
        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                notes.append(note)
            if isinstance(note, music21.chord.Chord):
                chord_notes = note._notes
                for chord_note in chord_notes:
                    if isinstance(chord_note, music21.note.Note):
                        new_note = chord_note
                        new_note.offset += note.offset
                        new_note.quarterLength = note.quarterLength
                        notes.append(new_note)

        print(notes)

        for note in notes:
            if isinstance(note, music21.note.Note):
                screen_x = self.viz_manager.main_frame.display.size.x
                screen_y = self.viz_manager.main_frame.display.size.y
                rect = self.viz_manager.GraphNoteRect(notes, note, pygame.Rect(0, 0, screen_x, screen_y - 20))
                print(rect)
                note_rect = Unit.NoteRect(rect, note)
                random.seed()
                color = (0, random.randint(50, 100), random.randint(150, 200))
                note_rect.color = color
                self.viz_manager.units.append(note_rect)
                print(self.viz_manager.units)
                # pygame.draw.rect(self.viz_manager.screen, (0, 50, 150), rect)


    def OnPlay(self, score):
        pass

    def PerMessage(self, screen, message):
        print("NOTE DOWN " + str(message.name))
