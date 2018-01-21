#!/usr/bin/env python
import mido
import music21

class MidiBlock:
    """
    This class contains all the information about the song ready
    to be used to create a visualization. Consider it the current
    'song state' of the song currently loaded, if a song is loaded.

    """

    def __init__(self, song_path=""):

        # Path of the song loaded, default is empty string.
        self.song_path = song_path

        # Mido object of the song.
        self.file_mido = None

        # Music21 object of the song.
        self.file_score = None

        self.load_song_to_block(self.song_path)

    def load_song_to_block(self, path):
        """
        Loads the block with the song from the given path, if possible.

        """
        self.song_path = path
        self.file_mido = mido.MidiFile(self.song_path)
        self.file_score = music21.midi.translate.midiFilePathToStream(self.song_path)

    def get_song_path(self):
        """
        Returns song file path.

        """
        return self.song_path

    def get_mido(self):
        """
        Returns the mido object of the song, if possible.

        """
        return self.file_mido

    def get_score(self):
        """
        Returns the music21 score object of the song, if possible.

        """
        return self.file_score

    def is_empty(self):
        """
        Returns true if no song is loaded, false if there is.

        """
        if self.song_path == (None or ""):
            return True
        return False
