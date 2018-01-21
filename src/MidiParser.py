#!/usr/bin/env python
import src.MidiBlock as mb

class MidiParser:
    """
    This class is responsible for reading a given compatible MIDI file and
    storing it in memory as a MidiBlock object.

    """

    def __init__(self):

        # Memory block of whatever song is currently loaded, None if no song is loaded.
        self.song_block = None

    def parse_file(self, string_path):
        """
        Reads file at given path, if possible, and saves as an object.

        :param string_path: string
            String of the path of the file (in the C: drive)

        """
        self.song_block = mb.MidiBlock(string_path)

    def get_song_block(self):
        """
        Returns song block.

        """
        return self.song_block

    def del_block(self):
        """
        Removes song block from memory.

        """
        pass
