#!/usr/bin/env python
import music21, time, pygame, pygame.midi

class Player:
    def __init__(self):
        self.bpm = 120

    def LoadSoundFont(self, sf):
        pass

    def PlayNote(self, note, beats):
        seconds = beats / self.bpm