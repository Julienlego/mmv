#!/usr/bin/env python
import music21, time, pygame, pygame.midi

class Player:

    def __init__(self):
        pygame.midi.init()
        self.__player = pygame.midi.Output(0)
        # Instruments for each track
        self.instrument = []
        for i in range(16):
            self.instrument.append(0)

    def __del__(self):
        pygame.midi.quit()

    def SetInstrument(self, instrument_id=0, channel=0):
        self.__player.set_instrument(instrument_id, channel)

    def NoteOn(self, midi_note=0, velocity=0, channel=0):
        self.__player.note_on(midi_note, velocity)

    def NoteOff(self, midi_note=0, velocity=0, channel=0):
        self.__player.note_off(midi_note, velocity, channel)


    # def LoadSoundFont(self, sf):
    #     pass

    # def PlayNote(self, note, beats):
    #     seconds = beats / self.bpm