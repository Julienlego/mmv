#!/usr/bin/env python
import time
import fluidsynth
import mingus
from music21 import *
import src.Preset as pr
import src.MidiParser as mp
import music21
import wx
import pygame

class VizManager:
    """
    This class manages the entire visualization system, including
    midi parsing and all the presets.
    """

    def __init__(self, main_frame, screen):
        # Preset that is currently loaded
        self.preset = None
        # Stores all presets
        self.presets = {}
        # Pygame screen object of the display
        self.screen = screen
        self.main_frame = main_frame
        # Current frame of the visualization
        self.curr_frame = None  # 0, if a song or preset is loaded
        # the parser for the midi file
        self.parser = mp.MidiParser()

        # a string to hold the path of the file that is currently open
        self.file_path = None

        # the list of units to draw to the screen
        self.units = []

        # Init and load all presets
        self.LoadPresets()
        self.LoadPreset("Default")     # load the default preset by default (so we don't have to select it manually)

    def LoadPresets(self):
        """
        Loads all presets.
        """
        # Create the preset!
        default = pr.SimpleCirclePreset(self, "Default", "This is a default visualization preset.")
        piano_static = pr.StaticPianoRollPreset(self, "Piano Roll Static", "This is a static piano roll preset.")

        # Add the preset to the dictionary!
        self.presets.update({default.name: default})
        self.presets.update({piano_static.name: piano_static})

    def LoadPreset(self, key):
        """
        Loads preset with key.
        """
        self.preset = self.presets[key]

    def LoadSongFromPath(self, path):
        """
        Reads file at given path, if possible, and saves as an object.
        """
        bsy = wx.BusyInfo("Loading song from path: " + path)
        self.parser.ParseFile(path)
        self.file_path = path
        tempo = self.parser.GetTempo()
        self.main_frame.statusbar.SetStatusText("Tempo: " + str(tempo) + " bpm", 2)
        bsy = None

    def Play(self):
        """
        Starts playing the visualization from the beginning.
        """
        self.preset.OnFirstLoad(self.parser.score)

        data = self.parser.score.parts[0]
        self.main_frame.debugger.WriteLine("Note/Rest\tOctave\tLen\tOffset\n")
        notes = [i for i in data.flat.notesAndRests]
        # Iterates through all notes and rests
        for n in notes:
            if isinstance(n, note.Note):
                line = str(n.pitch.name) + "\t" \
                       + str(n.pitch.octave) + "\t" \
                       + str(n.quarterLength) + "\t" \
                       + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            elif isinstance(n, note.Rest):
                line = "Rest" + "\t" \
                       + str(n.quarterLength) + "\t" \
                       + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            self.preset.PerMessage(self.screen, n)

        # self.parser.PlayFile(self.file_path)

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def GraphNoteRect(self, score, notee, dest):
        """
        Graphs a note onto a destination rect. Used for the static piano roll preset.

        :param score:   the score object of the song the note belongs to
        :param notee:   the note that is being graphed
        :param dest:    the destination rect to graph the note onto
        :return:        the rect that will represent the note within the destination rect
        """

        if not isinstance(notee, music21.note.Note):
            return None

        # get the highest and lowest notes for position normalization
        highest_note = 0
        lowest_note = float("inf")
        for n in score.flat.notes:
            if isinstance(n, music21.note.Note):
                if n.pitch.midi > highest_note:
                    highest_note = n.pitch.midi
                if n.pitch.midi < lowest_note:
                    lowest_note = n.pitch.midi

        largest_offset = score.flat.notes[len(score.flat.notes) - 1].offset
        number = notee.pitch.midi
        x = dest.left + dest.width * float(notee.offset / largest_offset)
        y = dest.top + (dest.height - (((number - lowest_note) / (highest_note - lowest_note)) * dest.height))
        print(str(x) + ", " + str(y))
        w = (dest.left + dest.width * float(notee.quarterLength / score.flat.notes[len(score.flat.notes) - 1].offset))
        h = 20
        rect = pygame.Rect(x, y, w, h)
        return rect
