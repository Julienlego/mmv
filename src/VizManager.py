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
import pygame.midi
import src.Utilities as util

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

        # the tempo of the song
        self.tempo = 0

        # the start time of the song, in ticks
        self.start_time = 0

        # bool for if the song is playing
        self.playing = False

        # bool for if the song should play
        self.should_play = False

        # a string to hold the path of the file that is currently open
        self.file_path = None

        # the list of units to draw to the screen
        self.units = []

        # the list of notes in the currently open file
        self.notes = []

        # the list of the currently playing notes
        # it is a tuple. first value is note, second is the tick it was played on
        self.current_notes = []

        # the list of the next notes to be played (more than 1 if they occur simultaneously)
        # it is a tuple. first value is note, second is the tick it should play on
        self.next_notes = []

        # the offset of the last note in the song
        self.last_offset = 0.

        # the midi player
        pygame.midi.init()
        self.player = pygame.midi.Output(0)

        # Init and load all presets
        self.LoadPresets()

    def LoadPresets(self):
        """
        Create and loads all presets.
        """
        # Create the preset!
        default = pr.SimpleCirclePreset(self, "Default", "This is a default visualization preset.")
        piano_roll = pr.PianoRollPreset(self, "Piano Roll", "This is a piano roll preset")
        piano_static = pr.StaticPianoRollPreset(self, "Piano Roll Static", "This is a static piano roll preset.")

        # Add the preset to the dictionary!
        self.presets.update({default.name: default})
        self.presets.update({piano_roll.name: piano_roll})
        self.presets.update({piano_static.name: piano_static})

    def LoadPreset(self, key):
        """
        Load preset with given key.
        """
        self.preset = self.presets[key]

    def LoadSongFromPath(self, path):
        """
        Reads file at given path, if possible, and saves as an object.
        """
        bsy = wx.BusyInfo("Loading song from path: " + path)
        self.parser.ParseFile(path)
        self.file_path = path
        self.units.clear()
        self.tempo = self.parser.GetTempo()
        self.main_frame.statusbar.SetStatusText("Tempo: " + str(self.tempo) + " bpm", 2)
        bsy = None

    def Play(self):
        """
        Starts playing the visualization from the beginning.
        """
        bsy = wx.BusyInfo("Initial Loading...")
        self.preset.OnFirstLoad(self.parser.score)
        bsy = None

        part = self.parser.score.parts[0]   # Gets first track/part of song

        # Prints all notes/rests in part to debug panel
        #self.main_frame.debugger.WriteLine("Note/Rest\tOctave\tLen\tOffset\n")
        notes = [i for i in part.flat.notesAndRests]
        # Iterates through all notes and rests
        for n in notes:
            if isinstance(n, note.Note):
                util.PrintNoteToPanel(self.main_frame.debugger, n)
                #self.main_frame.debugger.WriteLine(line)
                self.notes.append(n)
            elif isinstance(n, note.Rest):
                line = "Rest" + "\t" \
                       + str(n.duration.quarterLength) + "\t" \
                       + str(n.offset) + "\n"
                #self.main_frame.debugger.WriteLine(line)
            elif isinstance(n, chord.Chord):
                chord_notes = n._notes
                line = "=============chord=============\n"
                for chord_note in chord_notes:
                    if isinstance(chord_note, note.Note):
                        new_note = chord_note
                        new_note.offset = n.offset
                        new_note.quarterLength = n.quarterLength
                        #line += str(new_note.pitch.name) + "\t" \
                        #    + str(new_note.pitch.octave) + "\t" \
                        #    + str(new_note.duration.quarterLength) + "\t" \
                        #    + str(new_note.offset) + "\n"
                        self.notes.append(new_note)
                #line += "=============chord=============\n"
                util.PrintChordToPanel(self.main_frame.debugger, n)
                #print(line)
                #self.main_frame.debugger.WriteLine(line)
            # self.preset.PerMessage(self.screen, n)
        #self.main_frame.debugger.WriteLine("\n\n")
        #self.main_frame.debugger.WriteLine("===============================")


        self.should_play = True

        # get the offset of the first note in the song
        # so we can put it in next_notes
        first_offset = self.notes[0].offset
        for n in self.notes:
            if n.offset == first_offset:
                ticks = pygame.time.get_ticks()
                new_next_note = [n]
                new_next_note.append(ticks + util.OffsetMS(n.offset, self.tempo))
                self.next_notes.append(new_next_note)
            if n.offset > self.last_offset:
                self.last_offset = n.offset

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def Update(self):
        if not self.playing:
            if self.should_play:
                self.should_play = False
                self.playing = True
                self.start_time = pygame.time.get_ticks()
            return
        # determine whether or not to play something
        ticks = pygame.time.get_ticks()
        if self.next_notes != None:
            if ticks >= self.next_notes[0][1]:
                #print("NEXT NOTES AMOUNT: " + str(len(self.next_notes)))
                # move next_notes to current_notes
                for n in self.next_notes:
                    new_current_note = [n[0]]
                    # new_current_note.append(None)
                    self.current_notes.append(new_current_note)
                self.next_notes.clear()

                # get the next new notes
                current_offset = self.current_notes[0][0].offset
                if current_offset < self.last_offset:
                    for n in self.notes:
                        if n.offset > current_offset:
                            new_offset = n.offset
                            for m in self.notes:
                                if m.offset == new_offset:
                                    ticks = pygame.time.get_ticks()
                                    new_next_note = [m]
                                    new_next_note.append(ticks + util.OffsetMS((m.offset - current_offset), self.tempo))
                                    self.next_notes.append(new_next_note)
                            break

                # if we have reached the last note(s), set next_notes to none so we know not to keep checking for more
                else:
                    self.next_notes = None

                # set the ticks length of each current note and
                # play the note and draw it to the screen (via preset)
                for n in self.current_notes:
                    length = n[0].quarterLength
                    length_ms = util.OffsetMS(length, self.tempo)
                    n.append(length_ms)
                    self.player.note_on(n[0].pitch.midi, n[0].volume.velocity)
                    self.preset.PerMessage(self.screen, n[0])
                self.current_notes.clear()
