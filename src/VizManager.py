#!/usr/bin/env python
import time
import fluidsynth
import src.MidiParser as mp
import src.PresetManager as pm

class VizManager:
    """
    This class manages the entire visualization system, including
    midi parsing and all the presets.

    """

    def __init__(self):

        # Preset of visualization being used.
        self.preset = None

        # Stores all presets
        self.presets = {}

        # Midi Parser
        self.parser = mp.MidiParser()

        # Preset Manager
        self.preset_manager = pm.PresetManager()

    def LoadPreset(self):
        """

        """
        pass

    def LoadSongFromPath(self, path):
        """
        Load and filepath to parser
        """
        print("Loading song from path %s", path)
        self.parser.ParseFile(path)

    def Play(self):
        """
        Starts playing the vizualization from the beginning
        """
        pass
