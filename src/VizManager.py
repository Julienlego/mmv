#!/usr/bin/env python
import time
import fluidsynth
from music21 import *
import src.Preset as pr

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
        for n in notes:
            if isinstance(n, note.Note):
                line = str(n.pitch.name) + separator + str(n.pitch.octave) + separator + str(n.quarterLength) + separator + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            elif isinstance(n, note.Rest):
                line = "Rest" + separator + str(n.quarterLength) + separator + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass
