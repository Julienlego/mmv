#!/usr/bin/env python
import music21
import src.MidiTimeline as mt
from src.Imports import *

class MidiParser:
    """
    This class is responsible for reading a given compatible MIDI file and
    storing it in memory as a MidiBlock object.

    """

    def __init__(self, viz_manager):

        # the VizManager object this instance belongs to
        self.viz_manager = viz_manager

        # Path of the song loaded, default is empty string.
        self.path = "No file detected"

        # Music21 object of the song.
        self.score = None

    def ParseFile(self, path):
        """
        Reads file at given path, if possible, and saves as an object.

        :param path: string
            String of the path of the file (in the C: drive)

        """
        print("parsing file")
        self.path = path
        self.score = music21.midi.translate.midiFilePathToStream(path)
        # print(self.score.secondsMap)
        self.viz_manager.SetStatusText("Tempo: " + str(self.GetTempo(self.score)) + " bpm", 2)


        timeline = mt.MidiTimeline()
        timeline.tempo = None

        for part in self.score.parts:
            print(part)
        for note in self.score.flat.notes:
            print(str(note) + str(note.offset))
        print("debug")

    def GetSongPath(self):
        """
        Returns song file path.

        """
        return self.path

    def GetScore(self):
        """
        Returns the music21 score object of the song, if possible.

        """
        return self.score

    def IsEmpty(self):
        """
        Returns true if no song is loaded, false if there is.

        """
        if self.path == (None or ""):
            return bool(True)
        else:
            return bool(False)

    def GetTempo(self, score):
        """
        Returns the tempo of the song, as a float. Takes a music21.stream.Score object as the argument.
        This function assumes there are no tempo changes within the file.
        """
        seconds = score.secondsMap[0]['durationSeconds']
        print(seconds)
        last_note = score.flat.notes[len(score.flat.notes) - 1]
        quarter_length = last_note.quarterLength
        offset = last_note.offset
        total_length = offset + quarter_length

        beats = (total_length - (total_length % 4)) + 4

        tempo = 60.0 / float(seconds / beats)

        return tempo
