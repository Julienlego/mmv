#!/usr/bin/env python
import music21

class MidiTimeline:
    """
    This class will contain all of the MIDI information that the program will use
    for every track. It is essentially a list of events for the program to iterate through.
    """

    def __init__(self):
        self.length = 0
        self.frames = None  # list of MidiFrame objects


class MidiFrame:
    """
    This will act as a single 'frame' of the MIDI timeline.
    """

    def __init__(self):
        self.index = None   # the index of the current frame. this may not be needed since this will be part of a list
        self.events = None  # list of MIDI events that occur on this frame

