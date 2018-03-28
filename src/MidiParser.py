#!/usr/bin/env python
import music21
import src.Utilities as util


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
        # a dictionary mapping each track to its proper instrument
        self.instruments = [0 for x in range(16)]

    def ParseNewFile(self, path):
        """
        Reads file at given path, if possible, and returns a music21 Score object.
        """
        self.path = path
        self.score = music21.midi.translate.midiFilePathToStream(path)
        self.GetInstrumentsFromScore()
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
        quarter_length = None
        the_note = None
        seconds = None
        for note in self.score.flat.notesAndRests:
            if note.quarterLength > 0.0:
                try:
                    seconds = note.seconds
                except music21.exceptions21.Music21Exception:
                    seconds = None
                if seconds is not None:
                    quarter_length = note.quarterLength
                    the_note = note
                    break

        if quarter_length is None or seconds is None:
            return self.GetTempoOld()

        full_quarter_length = seconds * (1.0 / quarter_length)
        tempo = 60.0 / full_quarter_length

        return tempo

    def GetTempoOld(self):
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

    def GetInstrumentsFromScore(self):
        """
        Extracts instruments from current score.
        """
        for part in self.score.parts:
            instr = part.getInstrument(returnDefault=False)     # extract instrument obj from part
            i = 0       # default instrument
            if instr.instrumentName in util.instruments:
                i = util.instruments[instr.instrumentName]      # get midi val of instrument
            j = list(self.score.parts).index(part)       # track index
            # print("Track {0} has midi instrument {1}".format(j, i))
            self.instruments[j] = i
