#!/usr/bin/env python
import music21


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
