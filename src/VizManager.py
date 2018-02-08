#!/usr/bin/env python
import time
import fluidsynth
import time
import mingus
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
        default = pr.BasicPreset(self, "Default", "This is a default visualization preset.")
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

    def NoteToColor(self, note):
        """
        Converts music21 Note to an RGB color tuple (R, G, B) between 0-255

        Original idea and source code found here:
            http://www.endolith.com/wordpress/2010/09/15/a-mapping-between-musical-notes-and-colors/
        """
        if isinstance(note, music21.note.Note):
            print("Converting note: ", note.name)
            w = note.frequency
            # Everything below here is copied!
            # colour
            if w >= 380 and w < 440:
                r = -(w - 440.) / (440. - 350.)
                g = 0.0
                b = 1.0
            elif w >= 440 and w < 490:
                r = 0.0
                g = (w - 440.) / (490. - 440.)
                b = 1.0
            elif w >= 490 and w < 510:
                r = 0.0
                g = 1.0
                b = -(w - 510.) / (510. - 490.)
            elif w >= 510 and w < 580:
                r = (w - 510.) / (580. - 510.)
                g = 1.0
                b = 0.0
            elif w >= 580 and w < 645:
                r = 1.0
                g = -(w - 645.) / (645. - 580.)
                b = 0.0
            elif w >= 645 and w <= 780:
                r = 1.0
                g = 0.0
                b = 0.0
            else:
                r = 0.0
                g = 0.0
                b = 0.0

            # intensity correction
            if (w >= 380) and (w < 420):
                SSS = 0.3 + 0.7 * (w - 350) / (420 - 350)
            elif w >= 420 and w <= 700:
                SSS = 1.0
            elif w > 700 and w <= 780:
                SSS = 0.3 + 0.7 * (780 - w) / (780 - 700)
            else:
                SSS = 0.0
            SSS *= 255

            return (int(SSS * r), int(SSS * g), int(SSS * b))