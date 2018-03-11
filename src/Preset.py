#!/usr/bin/env python
import pygame
import music21
import src.Utilities as util
import src.Unit as unit


class BasePreset:
    """
    This class is represents the basic preset class object that all
    presets inherit from. None of the methods are actually implemented in this class.

    """

    def __init__(self, viz_manager, name="", desc="A description goes here."):
        # Name of preset. Also used as the key for the preset in the dict.
        self.name = name
        # Description of the visualization preset.
        self.desc = desc
        # Reference to the viz manager
        self.viz_manager = viz_manager
        self.lowest_pitch = float("inf")
        self.highest_pitch = 0
        self.notes_played = []
        self.latest_chord = None

    def OnFirstLoad(self, score):
        """
        Runs once to gather and store any information relative to the
        song before each frame of the visualization is made.

        This will also draw anything that's static and is always displayed (i.e. grid lines).

        YOUR CODE GOES BELOW
        """
        pass

    def PerNoteOn(self, screen, message):
        """
        Draws given message.

        YOUR CODE GOES BELOW
        """
        pass

    def PerNoteOff(self, screen, message):
        """
        Event handler for note off event.
        :param screen: the screen to draw to
        :param message: the midi message of the note off event
        :return: none
        """
        pass

    def FindChordFromNote(self, viz_note):
        """
        Sees if the note belongs to a chord by looking for other notes played that have
        the same offset and are from the same track.

        Returns a chord object containing the notes that are in the chord. Returns Nonte
        if the note doesn't belong to a chord.
        """
        offset = viz_note.note.offset
        track = viz_note.track
        notes = []

        for vn in self.notes_played:
            if (vn.track == track) and (vn.note.offset == offset):
                notes.append(vn.note)

        if not notes: return None
        else: return music21.chord.Chord(notes)



class PresetTest(BasePreset):
    """
    For testing purposes.
    """
    def OnFirstLoad(self, score):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

    def PerNoteOn(self, screen, message):
        pass

    def PerNoteOff(self, screen, message):
        pass


#############################################################
#                                                           #
#              !!! PRESETS WITH CIRCLES !!!                 #
#                                                           #
#############################################################


class PresetSimpleColorCircleRelative(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determined by velocity
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)

    def PerNoteOn(self, screen, viz_note):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = util.SimpleNoteToColorTuple(viz_note)
        y = util.GraphNoteY(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        r = int(viz_note.note.volume.velocity) // 2
        circle = unit.CircleNoteUnit(screen_x // 2, 0, color, viz_note, r)
        circle = util.CreateUnitInCenterOfQuadrant(circle, (0, 0), (screen_x, screen_y))
        circle.y = y
        self.viz_manager.units.append(circle)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetSimpleColorCircleMaxPitch(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determined by the velocity
    """

    def PerNoteOn(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = util.SimpleNoteToColorTuple(note)
        y = util.GraphNoteY(viz_note, 255, 0, screen_y)
        r = int(note.volume.velocity) // 2
        circle = unit.CircleNoteUnit(screen_x // 2, 0, color, note, r)
        circle = util.CreateUnitInCenterOfQuadrant(circle, (0, 0), (screen_x, screen_y))
        circle.y = y
        self.viz_manager.units.append(circle)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetPianoRollFading(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)

    def PerNoteOn(self, screen, viz_note):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.GraphNoteY(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = util.GetRandColor()
        note_rect = unit.RectNoteUnit(screen_x // 2, y, color, viz_note, 200, 20)
        note_rect.x -= (note_rect.w // 2)  # subtracts half the width as the offset to make the unit center
        note_rect.fade = True
        note_rect.delete_after_fade = True
        self.viz_manager.units.append(note_rect)


class PresetPianoRoll(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)

    def PerNoteOn(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = util.GetRandColor()
        note_rect = unit.RectNoteUnit(screen_x // 2, y, color, note, 200, 20)
        note_rect = util.CreateUnitInCenterOfQuadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = y
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetMonochromePianoRoll(BasePreset):
    """
    Similar to PianoRoll, but in black-white monochrome.
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)
        self.viz_manager.screen.fill((0, 0, 255))

    def PerNoteOn(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = util.MidiToMonochrome(viz_note.note.pitch.midi)
        note_rect = unit.RectNoteUnit(0, 0, color, note, 200, 20)
        note_rect = util.CreateUnitInCenterOfQuadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = y
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetColorPianoRoll(BasePreset):
    """
    This is a basic piano roll preset, except with color.
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)

    def PerNoteOn(self, screen, viz_note):
        viz_note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = util.SimpleNoteToColorTuple(viz_note)
        note_rect = unit.RectNoteUnit((screen_x // 2) - 100, 0, color, viz_note, 200, 20)
        note_rect = util.CreateUnitInCenterOfQuadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = util.GraphNoteY(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        self.viz_manager.units.append(note_rect)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetStaticPianoRoll(BasePreset):
    """
    This is a static preset that graphs the entire song onto the screen in a piano roll fashion.
    This preset is good for looking at the whole song as a whole.
    """

    def OnFirstLoad(self, score):
        # graph each note on the screen based off of pitch, offset, and length
        self.viz_manager.screen.fill((0, 0, 0))
        notes = []
        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                notes.append(note)
            if isinstance(note, music21.chord.Chord):
                chord_notes = note._notes
                for chord_note in chord_notes:
                    if isinstance(chord_note, music21.note.Note):
                        new_note = chord_note
                        new_note.offset += note.offset
                        new_note.quarterLength = note.quarterLength
                        notes.append(new_note)

        for note in notes:
            if isinstance(note, music21.note.Note):
                screen_x = self.viz_manager.main_frame.display.size.x
                screen_y = self.viz_manager.main_frame.display.size.y
                rect = util.CreateNoteRect(notes, note, pygame.Rect(0, 0, screen_x, screen_y))
                color = util.GetRandColor()
                note_rect = unit.RectNoteUnit(rect.left, rect.top, color, note, rect.width, rect.height)
                self.viz_manager.units.append(note_rect)


class PresetTwoTrackColorPianoRoll(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """

    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)

    def PerNoteOn(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = util.SimpleNoteToColorTuple(note)

        # variables for note_rect sizes and y position
        y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, screen_y)
        w = 180
        h = 15

        # Put note in left or right part of the screen, depending on what track it belongs to
        # print("Track: {0}".format(viz_note.track))
        if viz_note.track is 2:
            note_rect = unit.RectNoteUnit(0, 0, color, note, w, h)
            note_rect = util.CreateUnitInCenterOfQuadrant(note_rect, (screen_x // 2, 0), (screen_x, screen_y))
            note_rect.y = y
            self.viz_manager.units.append(note_rect)
        elif viz_note.track is 1:
            note_rect = unit.RectNoteUnit(0, 0, color, note, w, h)
            note_rect = util.CreateUnitInCenterOfQuadrant(note_rect, (0, 0), (screen_x // 2, screen_y))
            note_rect.y = y
            self.viz_manager.units.append(note_rect)

        # Add white line down center of the screen
        line_unit = unit.LineUnit(screen_x // 2, 0, screen_x // 2, screen_y, (255, 255, 255), 1)
        self.viz_manager.units.append(line_unit)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetMultiTrackColorCircle(BasePreset):

    def __init__(self, viz_manager, name="", desc="A description goes here."):
        super().__init__(viz_manager, name, desc)
        self.num_tracks = 0


    def OnFirstLoad(self, score):
        self.lowest_pitch, self.highest_pitch = util.GetEdgePitches(score)
        self.num_tracks = len(score.parts)

    def PerNoteOn(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = util.SimpleNoteToColorTuple(note)
        r = 15
        circle_note = unit.CircleNoteUnit(0, 0, color, note, r)

        interval = screen_x // self.num_tracks

        # Add white line down center of the screen
        for i in range(0, screen_x, interval):
            line = unit.LineUnit(i, 0, i, screen_y, (255, 255, 255), 1)
            self.viz_manager.units.append(line)

        x = interval * (viz_note.track - 1)
        # print("Printing note {0} in track {1} in interval {2}".format(note, viz_note.track, x))
        circle_note = util.CreateUnitInCenterOfQuadrant(circle_note, (0, 0), ((x + interval), screen_y))
        # print("Circle note x={0}, y={1}".format(circle_note.x, circle_note.y))
        # circle_note.x += (self.num_tracks - 1) * interval
        circle_note.y = util.GraphNoteY(note, self.highest_pitch, self.lowest_pitch, screen_y)
        self.viz_manager.units.append(circle_note)

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetChordRoot(BasePreset):
    """
    This preset aims to detect chords being played and displays the root note of each chord.
    It also draws a piano roll visualization of the notes, just like normal piano roll.
    """

    def OnFirstLoad(self, score):

        notes = [music21.note.Note('A'), music21.note.Note('D'), music21.note.Note('F'), music21.note.Note('G')]
        print(notes)
        chord = util.GetChord(notes)
        print(chord)
        print("chord name: " + str(chord.commonName))
        print("third: " + str(chord.third))
        print("fifth: " + str(chord.fifth))
        print("full name: " + str(chord.fullName))
        print("pitched common name: " + str(chord.pitchedCommonName))
        print("quality: " + str(chord.quality))
        print("root: " + str(chord.root))


        for note in score.flat.notes:
            if isinstance(note, music21.note.Note):
                if note.pitch.midi > self.highest_pitch:
                    self.highest_pitch = note.pitch.midi
                if note.pitch.midi < self.lowest_pitch:
                    self.lowest_pitch = note.pitch.midi
            if isinstance(note, music21.chord.Chord):
                chord_notes = note._notes
                for chord_note in chord_notes:
                    if isinstance(chord_note, music21.note.Note):
                        if chord_note.pitch.midi > self.highest_pitch:
                            self.highest_pitch = chord_note.pitch.midi
                        if chord_note.pitch.midi < self.lowest_pitch:
                            self.lowest_pitch = chord_note.pitch.midi

    def PerNoteOn(self, screen, message):
        self.notes_played.append(message)
        recent_notes = util.GetRecentNotes(self.notes_played)
        chord = util.GetChord(recent_notes)
        chord_name = chord.pitchedCommonName
        dbg = self.viz_manager.main_frame.debugger.textbox
        s1 = str(chord_name)
        s2 = ""
        if isinstance(self.latest_chord, music21.chord.Chord):
            s2 = str(self.latest_chord.pitchedCommonName)
        if s1 != s2:
            self.latest_chord = chord
            print("new chord: " + str(chord_name))
            util.PrintLineToPanel(dbg, "new chord: " + str(chord_name) + "\n")
        else:
            util.PrintLineToPanel(dbg, "------")

        pass

    def PerNoteOff(self, screen, message):
        self.viz_manager.remove_unit(message.note)
