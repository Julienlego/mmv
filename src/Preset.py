#!/usr/bin/env python
import pygame
import music21
import src.Utilities as util
import src.Unit as unit
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

    def PerNoteOn(self, screen, message):
        """
        Draws given message.

        YOUR CODE GOES BELOW
        """
        pass

    def PerNoteOff(self, screen, message):
        """
        Event handler for note off event.
        :param screen: the screen to draw to
        :param message: the midi message of the note off event
        :return: none
        """
        pass


class PresetJustText(BasePreset):
    """

    """
    def OnFirstLoad(self, score):
        pass

    def PerNoteOn(self, screen, message):
        pass

    def PerNoteOff(self, screen, message):
        pass


class PresetSimpleCircle(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determined by velocity

    """

    def OnFirstLoad(self, score):
        pass

    def PerNoteOn(self, screen, message):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

        if isinstance(message, music21.note.Note):
            color = util.SimpleNoteToColorTuple(message)
            radius = 75
            y = int(screen_y / message.octave)
            pos = (screen_x // 2, y)

            pygame.draw.circle(screen, color, pos, radius)

    def PerNoteOff(self, screen, message):
        pass


class PresetPianoRollFading(BasePreset):
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

    def PerNoteOn(self, screen, message):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        rect = pygame.Rect(0, 0, screen_x, screen_y)
        y = util.GraphNoteY(message, self.highest_pitch, self.lowest_pitch, rect)
        random.seed()
        color = (0, random.randint(50, 100), random.randint(150, 200))
        note_rect = unit.RectNoteUnit(300, y, color, message, 200, 20)
        note_rect.fade = True
        note_rect.delete_after_fade = True
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        print("NOTE OFF")


class PresetPianoRoll(BasePreset):
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

    def PerNoteOn(self, screen, message):
        note = message.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        rect = pygame.Rect(0, 0, screen_x, screen_y)
        y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, rect)
        random.seed()
        color = [0, random.randint(50, 100), random.randint(150, 200)]
        note_rect = unit.RectNoteUnit(300, y, color, message, 200, 20)
        note_rect.fade = False
        note_rect.delete_after_fade = False
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)
        # print("NOTE OFF")


class PresetColorPianoRoll(BasePreset):
    """
    This is a basic piano roll preset, except with color.
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

    def PerNoteOn(self, screen, message):
        message = message.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        rect = pygame.Rect(0, 0, screen_x, screen_y)
        y = util.GraphNoteY(message, self.highest_pitch, self.lowest_pitch, rect)
        color = util.SimpleNoteToColorTuple(message)
        # print(color)
        note_rect = unit.RectNoteUnit(screen_x // 2, y, color, message, 200, 20)
        note_rect.fade = False
        note_rect.delete_after_fade = False
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


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

        for note in notes:
            if isinstance(note, music21.note.Note):
                screen_x = self.viz_manager.main_frame.display.size.x
                screen_y = self.viz_manager.main_frame.display.size.y
                rect = util.CreateNoteRect(notes, note, pygame.Rect(0, 0, screen_x, screen_y))
                random.seed()
                color = [0, random.randint(50, 100), random.randint(150, 200)]
                note_rect = unit.RectNoteUnit(rect.left, rect.top, color, note, rect.width, rect.height)
                self.viz_manager.units.append(note_rect)


class TwoTrackPianoRoll(BasePreset):
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

    def PerNoteOn(self, screen, message):
        note = message.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        random.seed()
        color = [0, random.randint(50, 100), random.randint(150, 200)]
        # color = util.SimpleNoteToColorTuple(message)
        if message.track is 1:
            rect = pygame.Rect(0, 0, screen_x, screen_y)
        else:
            rect = pygame.Rect(screen_x, 0, screen_x, screen_y)

        y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, rect)
        h = 200
        w = 20

        if message.track is 1:
            x = screen_x // 3 - 100
        else:
            x = (screen_x // 3) * 2 - 100

        note_rect = unit.RectNoteUnit(x, y, color, note, h, w)
        note_rect.fade = False
        note_rect.delete_after_fade = False
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)
