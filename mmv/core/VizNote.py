#!/usr/bin/env python
"""
This is a wrapper class for a music21.Note object which contains more useful information than what a single
music21.Note object would contain. This was implemented primarily to handle multitrack notes.
"""
import music21


class VizNote:

    def __init__(self, note):
        self.chord_in_beat = None
        self.chord_in_half_bar = None
        self.chord_in_bar = None

        if isinstance(note, music21.note.Note):
            self.note = note
        else:
            self.note = None

        self.track = -1

