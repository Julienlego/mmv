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
        Reads file at given path, if possible, and saves as an object.

        :param path: string
            String of the path of the file (in the C: drive)

        """
        self.path = path
        self.score = music21.midi.translate.midiFilePathToStream(path)

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