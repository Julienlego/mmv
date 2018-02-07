#!/usr/bin/env python
import music21
import src.MidiTimeline as mt
import pygame


class MidiParser:
    """
    This class is responsible for reading a given compatible MIDI file and storing it.
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
        """
        print("parsing file")
        self.path = path
        self.score = music21.midi.translate.midiFilePathToStream(path)
        # print(self.score.secondsMap)
        tempo = self.GetTempo(self.score)
        self.viz_manager.SetStatusText("Tempo: " + str(tempo) + " bpm", 2)

        return self.score




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
        if (self.path is (None or "")) or (self.score is None):
            return True
        else:
            return False

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
