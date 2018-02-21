#!/usr/bin/env python
import music21, pygame, wx


def NoteToColor(note):
    """
    Converts music21 Note to an RGB color tuple (R, G, B) between 0-255 and returns the tuple

    Original idea and source code found here:
        http://www.endolith.com/wordpress/2010/09/15/a-mapping-between-musical-notes-and-colors/
    """
    if isinstance(note, music21.note.Note):
        w = note.frequency
        # Everything below here is copied!
        # colour
        if (w >= 380) and (w < 440):
            r = -(w - 440.) / (440. - 350.)
            g = 0.0
            b = 1.0
        elif (w >= 440) and (w < 490):
            r = 0.0
            g = (w - 440.) / (490. - 440.)
            b = 1.0
        elif (w >= 490) and (w < 510):
            r = 0.0
            g = 1.0
            b = -(w - 510.) / (510. - 490.)
        elif (w >= 510) and (w < 580):
            r = (w - 510.) / (580. - 510.)
            g = 1.0
            b = 0.0
        elif (w >= 580) and (w < 645):
            r = 1.0
            g = -(w - 645.) / (645. - 580.)
            b = 0.0
        elif (w >= 645) and (w <= 780):
            r = 1.0
            g = 0.0
            b = 0.0
        else:
            r = 0.0
            g = 0.0
            b = 0.0

        # intensity correction
        if (w >= 380) and (w < 420):
            SSS = 0.3 + 0.7 * (w - 350) / (420 - 350)
        elif (w >= 420) and (w <= 700):
            SSS = 1.0
        elif (w > 700) and (w <= 780):
            SSS = 0.3 + 0.7 * (780 - w) / (780 - 700)
        else:
            SSS = 0.0
        SSS *= 255

        color = (int(SSS * r), int(SSS * g), int(SSS * b))
        return color


def ToRect(x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    return rect


def OffsetMS(offset, tempo):
    seconds_per_beat = 60.0 / tempo
    ms_per_beat = seconds_per_beat * 1000
    offset_ms = ms_per_beat * offset
    return offset_ms


def GraphNoteY(note, highest_note, lowest_note, dest):
    """
    Returns the height position
    """
    the_pitch = note.pitch.midi
    y = dest.top + (dest.height - (((the_pitch - lowest_note) / (highest_note - lowest_note)) * dest.height))
    return y


def GraphNoteRect(notes, the_note, dest):
    """
    Graphs a note onto a destination rect. Used for the static piano roll preset.

    :param score:   the score object of the song the note belongs to
    :param notee:   the note that is being graphed
    :param dest:    the destination rect to graph the note onto
    :return:        the rect that will represent the note within the destination rect
    """

    if not isinstance(the_note, music21.note.Note):
        return None

    # get the highest and lowest notes for position normalization
    highest_note = 0
    lowest_note = float("inf")
    for n in notes:
        if isinstance(n, music21.note.Note):
            if n.pitch.midi > highest_note:
                highest_note = n.pitch.midi
            if n.pitch.midi < lowest_note:
                lowest_note = n.pitch.midi

    last_note = notes[len(notes) - 1]
    largest_offset = last_note.offset
    number = the_note.pitch.midi
    x = dest.left + dest.width * float(the_note.offset / (largest_offset + last_note.quarterLength))
    y = dest.top + (dest.height - (((number - lowest_note) / (highest_note - lowest_note)) * dest.height))
    print(str(x) + ", " + str(y))
    w = (dest.left + dest.width * float(the_note.quarterLength / (largest_offset + last_note.quarterLength)))
    h = 20
    rect = pygame.Rect(x, y, w, h)
    return rect


def PrintSongToPanel(dbg, score):
    notes = [i for i in score.flat.notesAndRests]
    # Iterates through all notes, rests, and chords
    for n in notes:
        if isinstance(n, music21.note.Note):
            PrintNoteToPanel(dbg, n)

        elif isinstance(n, music21.note.Rest):
            PrintRestToPanel(dbg, n)

        elif isinstance(n, music21.chord.Chord):
            PrintChordToPanel(dbg, n)

    PrintLineToPanel(dbg, "\n\n===============================")


def PrintLineToPanel(txt_panel, line):
    """
    Write line to TextCtrl (debug) panel
    """
    if isinstance(txt_panel, wx.TextCtrl):
        txt_panel.AppendText(line)


def PrintNoteToPanel(panel, n):
    """
    Prints note's name, octave, quarterLength, and offset to the (debug) panel
    """
    if isinstance(panel, wx.TextCtrl):
        line = str(n.pitch.name) + "\t" \
               + str(n.pitch.octave) + "\t" \
               + str(n.duration.quarterLength) + "\t" \
               + str(n.offset) + "\n"
        panel.AppendText(line)


def PrintRestToPanel(panel, r):
    """
    Prints rest to the (debug) panel
    """
    if isinstance(panel, wx.TextCtrl):
        if isinstance(r, music21.note.Rest):
            line = "Rest" + "\t" \
                   + str(r.duration.quarterLength) + "\t" \
                   + str(r.offset) + "\n"
            panel.AppendText(line)


def PrintChordToPanel(panel, n):
    """
    Prints chord, with all its notes, to the (debug) panel
    """
    if isinstance(panel, wx.TextCtrl):
        if isinstance(n, music21.chord.Chord):
            chord_notes = n._notes
            line = "=============chord=============\n"
            for chord_note in chord_notes:
                if isinstance(chord_note, music21.note.Note):
                    new_note = chord_note
                    new_note.offset = n.offset
                    new_note.quarterLength = n.quarterLength
                    line += str(new_note.pitch.name) + "\t" \
                            + str(new_note.pitch.octave) + "\t" \
                            + str(new_note.duration.quarterLength) + "\t" \
                            + str(new_note.offset) + "\n"
            line += "===============================\n"
            panel.AppendText(line)
