#!/usr/bin/env python
import music21


class MidiParser:
    """
    This class is responsible for reading a given compatible MIDI file and
    storing it in memory as a MidiBlock object.

    """

    def __init__(self):
        # Path of the song loaded, default is empty string.
        self.path = "No file detected"
        # Music21 object of the song.
        self.score = None

    def ParseFile(self, path):
        """
        Reads file at given path, if possible, and returns a music21 Score object.
        """
        self.path = path
        self.score = music21.midi.translate.midiFilePathToStream(path)
        return self.score

    def IsEmpty(self):
        """
        Returns true if no song is loaded, false if there is.
        """
        if (self.path is (None or "")) or (self.score is None):
            return bool(True)
        else:
            return bool(False)

    def GetTempo(self):
        """
        Returns the tempo of the song, as a float. Takes a music21.stream.Score object as the argument.
        This function assumes there are no tempo changes within the file.
        """
        seconds = self.score.secondsMap[0]['durationSeconds']
        # print(seconds)
        last_note = self.score.flat.notes[len(self.score.flat.notes) - 1]
        quarter_length = last_note.quarterLength
        offset = last_note.offset
        total_length = offset + quarter_length
        beats = (total_length - (total_length % 4)) + 4
        tempo = int(60.0 / float(seconds / beats))
        return tempo
