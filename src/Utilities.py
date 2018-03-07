#!/usr/bin/env python
import music21, pygame, wx
import src.VizNote as vn
import src.Unit as unit
import random

#############################################################
#                                                           #
#   !!! THESE FUNCTIONS ARE FOR PRINTI TO DEBUG FRAME !!!   #
#                                                           #
#############################################################

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


#############################################################
#                                                           #
#         !!! THESE FUNCTIONS ARE FOR COLOR !!!             #
#                                                           #
#############################################################


def SimpleNoteToColorTuple(viz_note):
    """
    Converts music21 Note to an RGB color tuple (R, G, B) and returns the tuple.
    The colors are predetermined.
    """
    if isinstance(viz_note, vn.VizNote):
        note = viz_note.note
    else:
        note = viz_note

    if isinstance(note, music21.note.Note):
        note_name = note.name

    elif isinstance(note, music21.chord.Chord):
        psum = 0
        for p in note.pitches:
            psum += int(p.midi)
        avg = psum // len(note.pitches)
        np = music21.pitch.Pitch(avg)
        n = music21.note.Note(np)
        note_name = n.name

    else:
        print("COULD NOT CONVERT NOTE TO RGB: {0}".format(type(note)))
        return None

    # Remove unneccessary characters to get just the note name and # or -
    note_name = note_name.replace('~', '')
    note_name = note_name.replace('`', '')

    color = (255, 255, 255)         # white
    if note_name == 'F#':
        color = (174, 0, 0)         # dark red
    elif note_name == 'G' or note_name == 'G#':
        color = (255, 0, 0)         # red
    elif note_name == 'A':
        color = (255, 102, 0)       # orange-red
    elif note_name == 'B-':
        color = (255, 239, 0)       # yellow
    elif note_name == 'B':
        color = (153, 255, 0)       # chartreuse
    elif note_name == 'C':
        color = (40, 255, 0)        # lime
    elif note_name == 'C#':
        color = (0, 255, 242)       # aqua
    elif note_name == 'D':
        color = (0, 122, 255)       # sky blue
    elif note_name == 'D#':
        color = (5, 0, 255)         # blue
    elif note_name == 'E' or note_name == 'E-':
        color = (71, 0, 237)        # blue-ish
    elif note_name == 'F':
        color = (99, 0, 178)        # indigo
    # print("Converting note {0} to color {1}".format(note_name, color))
    return color


def MidiToMonochrome(midi_note):
    """
    Returns a monochrome color using the midi note value.
    """
    r = g = b = midi_note
    return (r, g, b)


def ChangeColorBrightness(color=(0, 0, 0), val=0):
    """
    Changes the brightness of the RGB color by an integer -255 <= val <= 255 and returns the color.
    """
    r = TruncateColorValue(color[0] + val)
    g = TruncateColorValue(color[1] + val)
    b = TruncateColorValue(color[2] + val)
    return (r, g, b)


def TruncateColorValue(val):
    """
    Makes sure the new color value is with the valid range of 0 <= val <= 255.
    """
    if val < 0:
        return 0
    elif val > 255:
        return 255


def GetRandColor():
    """
    Returns a random RGB color.
    """
    random.seed()
    return (0, random.randint(50, 100), random.randint(150, 200))


#############################################################
#                                                           #
#     !!! THESE FUNCTIONS ARE FOR GRAPHING NOTES !!!        #
#                                                           #
#############################################################


def OffsetMS(offset, tempo):
    """

    """
    seconds_per_beat = 60.0 / tempo
    ms_per_beat = seconds_per_beat * 1000
    offset_ms = ms_per_beat * offset
    return offset_ms


def GraphNoteY(note, highest_note, lowest_note, screen_height):
    """
    Returns the height position of a note's pitch relative to the lowest and highest possible notes.
    """
    if isinstance(note, vn.VizNote):
        pitch = note.note.pitch.midi
    else:
        pitch = note.pitch.midi
    y = int(screen_height - (((pitch - lowest_note) / (highest_note - lowest_note)) * screen_height))
    return y


def CreateUnitInCenterOfQuadrant(note_unit=None, top_left_pos=(0, 0), bottom_right_pos=(0, 0)):
    """
    Takes a NoteUnit and returns a new NoteUnit located in the center of the rectangle drawn with the
    top left and bottom right points. Each point is a tuple (x, y) of its position.
    """
    x_mid = (bottom_right_pos[0] - top_left_pos[0]) // 2
    y_mid = (bottom_right_pos[1] - top_left_pos[1]) // 2
    new_unit = note_unit
    offset = 0
    if isinstance(note_unit, unit.RectNoteUnit):
        offset = new_unit.w // 2
    elif isinstance(note_unit, unit.CircleNoteUnit):
        offset = note_unit.radius
    new_unit.x = x_mid - offset
    new_unit.y = y_mid
    return new_unit


#############################################################
#                                                           #
#          !!! THESE ARE HELPER FUNCTIONS !!!               #
#                                                           #
#############################################################


def CreateNoteRect(notes, the_note, dest):
    """
    Creates a note onto a destination rect. Used for the static piano roll preset.

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
    # print(str(x) + ", " + str(y))
    w = (dest.left + dest.width * float(the_note.quarterLength / (largest_offset + last_note.quarterLength)))
    h = 20
    rect = pygame.Rect(x, y, w, h)
    return rect


def GetEdgePitches(score):
    """
    Takes a score and returns the lowest and highest pitches in the song.
    """
    lowest = 0
    highest = 0
    for note in score.flat.notes:
        if isinstance(note, music21.note.Note):
            if note.pitch.midi > highest:
                highest = note.pitch.midi
            if note.pitch.midi < lowest:
                lowest = note.pitch.midi
        if isinstance(note, music21.chord.Chord):
            chord_notes = note._notes
            for chord_note in chord_notes:
                if isinstance(chord_note, music21.note.Note):
                    if chord_note.pitch.midi > highest:
                        highest = chord_note.pitch.midi
                    if chord_note.pitch.midi < lowest:
                        lowest = chord_note.pitch.midi
    return lowest, highest


def GetNotesList(score):
    current_offset = 0.0
    last_offset = 0.0
    track_num = 0
    tracks = []
    flat = []

    for element in score:
        # print("ELEMENT")
        # print(element)
        track_num += 1
        new_track = []
        instruments = element.getInstruments()
        for note in element.flat.notes:
            if isinstance(note, music21.note.Note):
                # print(note)
                new_viz_note = vn.VizNote(note)
                new_viz_note.track = track_num
                new_track.append(new_viz_note)

                if note.offset > last_offset:
                    last_offset = note.offset
            if isinstance(note, music21.chord.Chord):
                for n in note:
                    if isinstance(n, music21.note.Note):
                        # print(note)
                        n.offset += note.offset
                        new_viz_note = vn.VizNote(n)
                        new_viz_note.track = track_num
                        new_track.append(new_viz_note)

                        if note.offset > last_offset:
                            last_offset = note.offset
        tracks.append(new_track)
    # print(last_offset)

    for track in tracks:
        for note in track:
            flat.append(note)

    # print(len(flat))
    flat.sort(key=lambda x: x.note.offset)
    # print(flat)
    return flat


def GetChord(notes):
    note_names = []
    for note in notes:
        if isinstance(note, music21.note.Note):
            note_names.append(note.name)
        elif isinstance(note, vn.VizNote):
            note_names.append(note.note.name)

    if len(note_names) > 0:
        chord = music21.chord.Chord(note_names)
        return chord
    else:
        return None


def GetRecentNotes(notes, num=5):
    index = abs(num) * -1
    previous_notes = notes[index:]
    return previous_notes
