#!/usr/bin/env python
import pygame
import music21


class VizNote:
    """
    This is a wrapper class for a music21.Note object which contains more useful information than what a single
    music21.Note object would contain. This was implemented primarily to handle multitrack notes.
    """

    def __init__(self, note):
        if isinstance(note, music21.note.Note):
            self.note = note
        else:
            self.note = None

        self.track = -1

