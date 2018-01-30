#!/usr/bin/env python
import time
import fluidsynth
import wx
import src.MidiParser as mp
import src.Preset as pr

class VizManager:
    """
    This class manages the entire visualization system, including
    midi parsing and all the presets.
    """

    def __init__(self, pygame_screen):
        self.preset = None
        self.presets = {}
        self.parser = mp.MidiParser()
        self.screen = pygame_screen
        self.curr_frame = None  # 0, if a song or preset is loaded

    def LoadPresets(self):
        """
        Loads all presets.
        """
        self.presets["default"] = pr.BasicPreset()

    def LoadSongFromPath(self, path):
        """
        Load and filepath to parser.
        """
        print("Loading song from path %s", path)
        self.parser.ParseFile(path)

    def Play(self):
        """
        Starts playing the visualization from the beginning.
        """
        if self.preset is None:
            wx.MessageBox("No midi file was selected", "Missing File!", wx.OK | wx.ICON_ERROR)

        elif self.parser.IsEmpty() is True:
            wx.MessageBox("No preset was selected", "Missing Preset!", wx.OK | wx.ICON_ERROR)

        else:
            self.preset.OnFirstLoad()
            for line in self.parser.GetScore().parts:
                print(line)
                self.preset.PerMessage(line)


    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass
