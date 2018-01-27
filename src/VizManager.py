#!/usr/bin/env python
import src.MidiParser as mp
import src.PresetManager as pm

CONST_DEFAULT_SONG_PATH = "" #"C:\Users\Jules\Desktop\midifiles"

class VizManager:
    """
    This class manages the entire visualization system, including
    midi parsing and all the presets.

    """

    def __init__(self, panel):

        self.pygame_panel = panel

        # Preset of visualization being used.
        self.preset = None

        # Path of the midi song being used.
        self.song_path = None

        # List of each frame of the visualization.
        self.frames = []

        # Midi Parser
        self.song_parser = mp.MidiParser()

        # Preset Manager
        self.preset_manager = pm.PresetManager()

    def LoadPreset(self):
        pass

    def LoadSong(self, path):
        print("Loading song from path %s", path)
        self.song_parser.parse_file(path)

    def generate_viz(self):
        """
        Generate and capture each frame of the visualization

        """
        pass

    def goto_frame(self, frame_id):
        """

        """
        pass

    def __generate_frame(self):
        """
        Private method that uses the current preset to draw the frame of
        a midi message and capture its framebuffer.

        """
        pass
