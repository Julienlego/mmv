#!/usr/bin/env python
import music21
import pygame
import wx
import mmv.core.VizNote as vn
import mmv.core.Unit as unit

#############################################################
#                                                           #
#   !!! THESE FUNCTIONS ARE FOR PRINTI TO DEBUG FRAME !!!   #
#                                                           #
#############################################################


def print_song_to_panel(dbg, score):
    notes = [i for i in score.flat.notesAndRests]
    # Iterates through all notes, rests, and chords
    for n in notes:
        if isinstance(n, music21.note.Note):
            print_note_to_panel(dbg, n)

        elif isinstance(n, music21.note.Rest):
            print_rest_to_panel(dbg, n)

        elif isinstance(n, music21.chord.Chord):
            print_chord_to_panel(dbg, n)

    print_line_to_panel(dbg, "\n\n===============================")


def print_line_to_panel(txt_panel, line):
    """
    Write line to TextCtrl (debug) panel
    """
    if isinstance(txt_panel, wx.TextCtrl):
        txt_panel.WriteText(line)


def print_note_to_panel(panel, n):
    """
    Prints note's name, octave, quarterLength, and offset to the (debug) panel
    """
    if isinstance(panel, wx.TextCtrl):
        line = str(n.pitch.name) + "\t" \
               + str(n.pitch.octave) + "\t" \
               + str(n.duration.quarterLength) + "\t" \
               + str(n.offset) + "\n"
        print_line_to_panel(panel, line)


def print_rest_to_panel(panel, r):
    """
    Prints rest to the (debug) panel
    """
    if isinstance(panel, wx.TextCtrl):
        if isinstance(r, music21.note.Rest):
            line = "Rest" + "\t" \
                   + str(r.duration.quarterLength) + "\t" \
                   + str(r.offset) + "\n"
            print_line_to_panel(panel, line)


def print_chord_to_panel(panel, n):
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
            print_line_to_panel(panel, line)


#############################################################
#                                                           #
#     !!! THESE FUNCTIONS ARE FOR GRAPHING NOTES !!!        #
#                                                           #
#############################################################


def offet_ms(offset, tempo):
    """

    """
    seconds_per_beat = 60.0 / tempo
    ms_per_beat = seconds_per_beat * 1000
    offset_ms = ms_per_beat * offset
    return offset_ms


def graph_note_y(note, highest_note, lowest_note, screen_height, smart_crop=False):
    """
    Returns the height position of a note's pitch relative to the lowest and highest possible notes.
    """
    if isinstance(note, vn.VizNote):
        pitch = note.note.pitch.midi
    else:
        pitch = note.pitch.midi

    if smart_crop:
        lowest_note -= 1

    y = int(screen_height - (((pitch - lowest_note) / (highest_note - lowest_note)) * screen_height))

    return y


def create_unit_in_center_of_quadrant(note_unit=None, top_left_pos=(0, 0), bottom_right_pos=(0, 0)):
    """
    Takes a NoteUnit and returns a new NoteUnit located in the center of the rectangle drawn with the
    top left and bottom right points. Each point is a tuple (x, y) of its position.
    """
    x_mid = (bottom_right_pos[0] + top_left_pos[0]) // 2
    y_mid = (bottom_right_pos[1] + top_left_pos[1]) // 2
    new_unit = note_unit
    # Center the note using the offset
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
#      !!! THESE ARE HELPER FUNCTIONS FOR PRESETS!!!        #
#                                                           #
#############################################################


def create_note_rect(notes, the_note, dest):
    """
    Creates a note onto a destination rect. Used for the static piano roll preset.

    :param notes:   the score object of the song the note belongs to
    :param the_note:   the note that is being graphed
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


def get_edge_pitches(score):
    """
    Takes a score and returns the lowest and highest pitches in the song.
    """
    lowest = 255
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


def get_viz_notes(score):
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

    quarter_beats = flat[-1].note.offset
    quarter_beats = int(quarter_beats)

    bars = quarter_beats // 4
    half_bars = bars * 2

    # transcribing chords by quarter beat in song
    for i in range(0, quarter_beats):
        q_notes = []
        q_vnotes = []
        for note in flat:
            if float(i) <= note.note.offset < float(i + 1):
                q_notes.append(note.note)
                q_vnotes.append(note)
        chord = music21.chord.Chord(q_notes)

        for note in q_vnotes:
            note.chord_in_beat = chord

    # transcribing chords by half-bar in song
    for i in range(0, half_bars):
        hb_notes = []
        hb_vnotes = []
        for note in flat:
            if float(i * 2) <= note.note.offset < float((i + 1) * 2):
                hb_notes.append(note.note)
                hb_vnotes.append(note)
        chord = music21.chord.Chord(hb_notes)

        for note in hb_vnotes:
            note.chord_in_half_bar = chord

    # transcribing chords by bar in song
    for i in range(0, bars):
        b_notes = []
        b_vnotes = []
        for note in flat:
            if float(i * 4) <= note.note.offset < float((i + 1) * 4):
                b_notes.append(note.note)
                b_vnotes.append(note)
        chord = music21.chord.Chord(b_notes)

        for note in b_vnotes:
            note.chord_in_bar = chord

    return flat
