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
import src.Utilities as Util

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
        self.LoadPreset("Default")     # load the default preset by default (so we don't have to select it manually)

    def LoadPresets(self):
        """
        Loads all presets.
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
        self.units.clear()
        self.tempo = self.parser.GetTempo()
        self.main_frame.statusbar.SetStatusText("Tempo: " + str(self.tempo) + " bpm", 2)
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
                       + str(n.duration.quarterLength) + "\t" \
                       + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
                self.notes.append(n)
            elif isinstance(n, note.Rest):
                line = "Rest" + "\t" \
                       + str(n.duration.quarterLength) + "\t" \
                       + str(n.offset) + "\n"
                self.main_frame.debugger.WriteLine(line)
            elif isinstance(n, chord.Chord):
                chord_notes = n._notes
                line = "=============chord=============\n"
                for chord_note in chord_notes:
                    if isinstance(chord_note, note.Note):
                        new_note = chord_note
                        new_note.offset = n.offset
                        new_note.quarterLength = n.quarterLength
                        line += str(new_note.pitch.name) + "\t" \
                            + str(new_note.pitch.octave) + "\t" \
                            + str(new_note.duration.quarterLength) + "\t" \
                            + str(new_note.offset) + "\n"
                        self.notes.append(new_note)
                line += "=============chord=============\n"
                print(line)
                self.main_frame.debugger.WriteLine(line)

            # self.preset.PerMessage(self.screen, n)
        self.main_frame.debugger.WriteLine("\n\n")
        self.main_frame.debugger.WriteLine("===============================")

        self.should_play = True

        # get the offset of the first note in the song
        # so we can put it in next_notes
        first_offset = self.notes[0].offset
        for n in self.notes:
            if n.offset == first_offset:
                ticks = pygame.time.get_ticks()
                new_next_note = [n]
                new_next_note.append(ticks + Util.OffsetMS(n.offset, self.tempo))
                self.next_notes.append(new_next_note)
            if n.offset > self.last_offset:
                self.last_offset = n.offset



        # self.parser.PlayFile(self.file_path)

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
                print("NEXT NOTES AMOUNT: " + str(len(self.next_notes)))
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
                                    new_next_note.append(ticks + Util.OffsetMS((m.offset - current_offset), self.tempo))
                                    self.next_notes.append(new_next_note)
                            break

                # if we have reached the last note(s), set next_notes to none so we know not to keep checking for more
                else:
                    self.next_notes = None

                # set the ticks length of each current note
                for n in self.current_notes:
                    length = n[0].quarterLength
                    length_ms = Util.OffsetMS(length, self.tempo)
                    n.append(length_ms)
                    self.preset.PerMessage(self.screen, n[0], self.player)
                self.current_notes.clear()


    def GraphNoteRect(self, notes, the_note, dest):
        """
        Graphs a note onto a destination rect. Used for the static piano roll preset.

        :param score:   the score object of the song the note belongs to
        :param notee:   the note that is being graphed
        :param dest:    the destination rect to graph the note onto
        :return:        the rect that will represent the note within the destination rect
        """

        if not isinstance(the_note, music21.note.Note):
            return None

        # get the highest and lowest notes for position normalization
        highest_note = 0
        lowest_note = float("inf")
        for n in notes:
            if isinstance(n, music21.note.Note):
                if n.pitch.midi > highest_note:
                    highest_note = n.pitch.midi
                if n.pitch.midi < lowest_note:
                    lowest_note = n.pitch.midi

        last_note = notes[len(notes) - 1]
        largest_offset = last_note.offset
        number = the_note.pitch.midi
        x = dest.left + dest.width * float(the_note.offset / (largest_offset + last_note.quarterLength))
        y = dest.top + (dest.height - (((number - lowest_note) / (highest_note - lowest_note)) * dest.height))
        print(str(x) + ", " + str(y))
        w = (dest.left + dest.width * float(the_note.quarterLength / (largest_offset + last_note.quarterLength)))
        h = 20
        rect = pygame.Rect(x, y, w, h)
        return rect

    def GraphNoteY(self, note, highest_note, lowest_note, dest):
        the_pitch = note.pitch.midi
        y = dest.top + (dest.height - (((the_pitch - lowest_note) / (highest_note - lowest_note)) * dest.height))
        return y
