#!/usr/bin/env python
import time
import fluidsynth
import time
from music21 import *
import src.Preset as pr
from src.Imports import *
import music21

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
        # Path of the song loaded, default is empty string.
        self.path = "No file detected"
        # Music21 object of the song.
        self.score = None
        # Pygame screen object of the display
        self.screen = screen
        self.main_frame = main_frame
        # Current frame of the visualization
        self.curr_frame = None  # 0, if a song or preset is loaded

        self.midi_parser = src.MidiParser.MidiParser(self)      # the parser for the midi file

        self.LoadPresets()

        self.LoadPreset("Default")     # load the default preset by default (so we don't have to select it manually)

    def LoadPresets(self):
        """
        Loads all presets.
        """
        # Create the preset!
        default = pr.BasicPreset("Default", "This is a default visualization preset.")

        # Add the preset to the dictionary!
        self.presets.update({default.name: default})

    def LoadPreset(self, key):
        """
        Loads preset with key.
        """
        self.preset = self.presets[key]

    def LoadSongFromPath(self, path):
        """
        Reads file at given path, if possible, and saves as an object.
        """
        print("Loading song from path: ", path)
        self.path = path
        self.score = midi.translate.midiFilePathToStream(path)
        print(type(self.score))
        self.midi_parser.ParseFile(path)

    def IsSongLoaded(self):
        """
        Returns true if no song is loaded, false if there is.
        """
        if (self.path is (None or "")) or (self.score is None):
            return True
        else:
            return False

    def Play(self):
        """
        Starts playing the visualization from the beginning.
        """
        self.preset.OnFirstLoad(self.score)

        data = self.score.parts[0]
        self.main_frame.debugger.WriteLine("Note/Rest\tOctave\tLen\tOffset\n")
        notes = [i for i in data.flat.notesAndRests]
        separator = "\t"
        # Iterates through all notes and rests
        for n in notes:
            if isinstance(n, note.Note):
                line = str(n.pitch.name) + separator + str(n.pitch.octave) + separator + str(n.quarterLength) + separator + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            elif isinstance(n, note.Rest):
                line = "Rest" + separator + str(n.quarterLength) + separator + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            msg = ""
            self.preset.PerMessage(self.screen, msg)

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def SetStatusText(self, text, pos):
        self.main_frame.statusbar.SetStatusText(text, pos)

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
        width = (dest.left + dest.width * float(notee.quarterLength / score.flat.notes[len(score.flat.notes) - 1].offset))
        height = 20

        rect = (x, y, width, height)
        return rect


