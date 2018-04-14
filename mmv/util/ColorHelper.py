#!/usr/bin/env python
#############################################################
#                                                           #
#         !!! THESE FUNCTIONS ARE FOR COLOR !!!             #
#                                                           #
#############################################################
import random
import music21
import mmv.core.VizNote as vn


def simple_note_to_color_tuple(viz_note, key=None):
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

    # Remove unnecessary characters to get just the note name and # or -
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


def scale_degree_to_color(note, key=None):
    """
    :param note:
    :param key:
    :return:
    """
    note_colors = {
        0: (255, 0, 0),
        1: (255, 100, 0),
        2: (255, 150, 0),
        3: (255, 200, 0),
        4: (255, 255, 0),
        5: (0, 255, 0),
        6: (0, 255, 255),
        7: (0, 0, 255),
        8: (100, 0, 255),
        9: (200, 0, 255),
        10: (255, 0, 255),
        11: (255, 100, 255)}

    if isinstance(note, music21.note.Note):
        sd = note.pitch.midi
    else:
        return (255, 255, 255)

    sd = sd % 12

    if key is not None:
        tonic_pitch = key.tonic.pitchClass
        relative_pitch = (sd - tonic_pitch) % 12

        color = note_colors[relative_pitch]
        return color
    else:
        color = note_colors[sd]
        return color


def midi_to_monochrome(midi_note):
    """
    Returns a monochrome color using the midi note value.
    """
    r = g = b = midi_note
    return (r, g, b)


def change_color_brightness(color=(0, 0, 0), val=0):
    """
    Changes the brightness of the RGB color by an integer -255 <= val <= 255 and returns the color.
    """
    r = truncate_color_value(int(color[0] + val))
    g = truncate_color_value(int(color[1] + val))
    b = truncate_color_value(int(color[2] + val))
    nc = (r, g, b)
    return nc


def truncate_color_value(val):
    """
    Makes sure the new color value is with the valid range of 0 <= val <= 255.
    """
    if val < 0:
        return 0
    elif val > 255:
        return 255
    else:
        return val


def get_rand_color():
    """
    Returns a random RGB color.
    """
    random.seed()
    return (0, random.randint(50, 100), random.randint(150, 200))
