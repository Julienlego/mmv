#!/usr/bin/env python
"""

"""
import pygame
import music21
import mmv.util.Utilities as util
import math
import mmv.core.Unit as unit
import mmv.util.ColorHelper as colorhelper
import mmv.util.MusicComp as muse


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
        self.key = None
        self.num_tracks = 0

    def first_load(self, score):
        """
        Runs once to gather and store any information relative to the
        song before each frame of the visualization is made.

        This will also draw anything that's static and is always displayed (i.e. grid lines).

        YOUR CODE GOES BELOW
        """
        pass

    def per_note_on(self, screen, message):
        """
        Draws given message.

        YOUR CODE GOES BELOW
        """
        pass

    def per_note_off(self, screen, message):
        """
        Event handler for note off event.
        :param screen: the screen to draw to
        :param message: the midi message of the note off event
        :return: none
        """
        pass


class PresetTest(BasePreset):
    """
    For testing purposes.
    """
    def first_load(self, score):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

    def per_note_on(self, screen, message):
        pass

    def per_note_off(self, screen, message):
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

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(viz_note)
        y = util.graph_note_y(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        r = int(viz_note.note.volume.velocity) // 2
        circle = unit.CircleNoteUnit(screen_x // 2, 0, color, viz_note, r)
        circle.id = id(viz_note)
        circle = util.create_unit_in_center_of_quadrant(circle, (0, 0), (screen_x, screen_y))
        circle.y = y
        self.viz_manager.units.append(circle)

    def per_note_off(self, screen, viz_note):
        self.viz_manager.remove_unit(viz_note.note, id(viz_note))


class PresetSimpleColorCircleMaxPitch(BasePreset):
    """
    This is a basic preset that draws a circle randomly on the screen for each midi event.

    For each event:
        - color is determined by note
        - radius of circle is determined by the velocity
    """

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(note)
        y = util.graph_note_y(viz_note, 255, 0, screen_y)
        r = int(note.volume.velocity) // 2
        circle = unit.CircleNoteUnit(screen_x // 2, 0, color, note, r)
        circle = util.create_unit_in_center_of_quadrant(circle, (0, 0), (screen_x, screen_y))
        circle.y = y
        self.viz_manager.units.append(circle)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetPianoRollFading(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.graph_note_y(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = colorhelper.get_rand_color()
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

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = colorhelper.get_rand_color()
        note_rect = unit.RectNoteUnit(screen_x // 2, y, color, note, 200, 20)
        note_rect = util.create_unit_in_center_of_quadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = y
        self.viz_manager.units.append(note_rect)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetMonochromePianoRoll(BasePreset):
    """
    Similar to PianoRoll, but in black-white monochrome.
    """

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.viz_manager.screen.fill((0, 0, 255))

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        color = colorhelper.midi_to_monochrome(viz_note.note.pitch.midi)
        note_rect = unit.RectNoteUnit(0, 0, color, note, 200, 20)
        note_rect = util.create_unit_in_center_of_quadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = y
        self.viz_manager.units.append(note_rect)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetColorPianoRoll(BasePreset):
    """
    This is a basic piano roll preset, except with color.
    """

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        viz_note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(viz_note)
        note_rect = unit.RectNoteUnit((screen_x // 2) - 100, 0, color, viz_note, 200, 20)
        note_rect = util.create_unit_in_center_of_quadrant(note_rect, (0, 0), (screen_x, screen_y))
        note_rect.y = util.graph_note_y(viz_note, self.highest_pitch, self.lowest_pitch, screen_y)
        self.viz_manager.units.append(note_rect)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetStaticPianoRoll(BasePreset):
    """
    This is a static preset that graphs the entire song onto the screen in a piano roll fashion.
    This preset is good for looking at the whole song as a whole.
    """

    def first_load(self, score):
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
                rect = util.create_note_rect(notes, note, pygame.Rect(0, 0, screen_x, screen_y))
                color = colorhelper.get_rand_color()
                note_rect = unit.RectNoteUnit(rect.left, rect.top, color, note, rect.width, rect.height)
                self.viz_manager.units.append(note_rect)


class PresetTwoTrackColorPianoRoll(BasePreset):
    """
    This is a basic piano roll preset.
    Each note is drawn onto the screen in a piano roll fashion.
    Notes with greater pitch go higher on the screen, lower notes go lower.
    """
    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(note)

        # variables for note_rect sizes and y position
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        w = 180
        h = 15

        # Put note in left or right part of the screen, depending on what track it belongs to
        # print("Track: {0}".format(viz_note.track))
        if viz_note.track is 2:
            note_rect = unit.RectNoteUnit(0, 0, color, note, w, h)
            note_rect = util.create_unit_in_center_of_quadrant(note_rect, (screen_x // 2, 0), (screen_x, screen_y))
            note_rect.y = y
            self.viz_manager.units.append(note_rect)
        elif viz_note.track is 1:
            note_rect = unit.RectNoteUnit(0, 0, color, note, w, h)
            note_rect = util.create_unit_in_center_of_quadrant(note_rect, (0, 0), (screen_x // 2, screen_y))
            note_rect.y = y
            self.viz_manager.units.append(note_rect)

        # Add white line down center of the screen
        line_unit = unit.LineUnit(screen_x // 2, 0, screen_x // 2, screen_y, (255, 255, 255), 1)
        self.viz_manager.units.append(line_unit)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetMultiTrackColorCircle(BasePreset):
    """
    This preset draws notes in each track as circles, where the each track has its own column on the screen.
    """
    def __init__(self, viz_manager, name, desc):
        super().__init__(viz_manager, name, desc)
        self.num_tracks = 0

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.num_tracks = len(score.parts)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(note)
        r = 15
        circle_note = unit.CircleNoteUnit(0, 0, color, note, r)

        interval = screen_x // self.num_tracks

        # Add white line down center of the screen
        for i in range(0, screen_x, interval):
            line = unit.LineUnit(i, 0, i, screen_y, (255, 255, 255), 1)
            self.viz_manager.units.append(line)

        x = interval * (viz_note.track - 1)
        # print("Printing note {0} in track {1} in interval {2}".format(note, viz_note.track, x))
        circle_note = util.create_unit_in_center_of_quadrant(circle_note, (0, 0), ((x + interval), screen_y))
        # print("Circle note x={0}, y={1}".format(circle_note.x, circle_note.y))
        # circle_note.x += (self.num_tracks - 1) * interval
        circle_note.y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        self.viz_manager.units.append(circle_note)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetMultiTrackColorPianoRoll(BasePreset):
    """

    """
    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.num_tracks = len(score.parts)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(note)
        track_width = screen_x // self.num_tracks

        h = screen_y // (self.highest_pitch - (self.lowest_pitch - 1))
        rect_note = unit.RectNoteUnit(0, 0, color, note, track_width, h)
        rect_note.id = id(viz_note)     # this is an important line!

        region_x = track_width * (viz_note.track - 1)
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y, True)

        rect_note = util.create_unit_in_center_of_quadrant(rect_note, (region_x, 0), (region_x + track_width, screen_y))
        rect_note.y = y

        self.viz_manager.units.append(rect_note)

    def per_note_off(self, screen, viz_note):
        self.viz_manager.remove_unit(viz_note.note, id(viz_note))


class PresetMultiTrackChords(BasePreset):
    """

    """
    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.num_tracks = len(score.parts)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.scale_degree_to_color(note, self.viz_manager.key)
        track_width = screen_x // self.num_tracks

        h = screen_y // (self.highest_pitch - (self.lowest_pitch - 1))
        rect_note = unit.RectNoteUnit(0, 0, color, note, track_width, h)
        rect_note.id = id(viz_note)

        region_x = track_width * (viz_note.track - 1)
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y, True)

        rect_note = util.create_unit_in_center_of_quadrant(rect_note, (region_x, 0), (region_x + track_width, screen_y))
        rect_note.y = y

        self.viz_manager.units.append(rect_note)

        # chord stuff
        self.notes_played.append(viz_note)
        recent_notes = muse.get_recent_notes(self.notes_played)
        chord = muse.get_chord(recent_notes)
        chord_name = chord.pitchedCommonName
        s1 = str(chord_name)
        s2 = ""
        if isinstance(self.latest_chord, music21.chord.Chord):
            s2 = str(self.latest_chord.pitchedCommonName)
        if s1 != s2:
            print("new chord: " + str(chord_name))

            if self.latest_chord is None:
                self.latest_chord = chord

            root = self.latest_chord.root()
            note = music21.note.Note(root)
            self.viz_manager.remove_unit(note, id(note), type(unit.RectChordUnit))

            self.latest_chord = chord
            root = self.latest_chord.root()
            note = music21.note.Note(root)

            color = colorhelper.scale_degree_to_color(note, self.viz_manager.key)
            rect_chord = unit.RectChordUnit(0, 0, color, note, screen_x, screen_y, 20)
            rect_chord.id = id(note)

            self.viz_manager.units.append(rect_chord)

    def per_note_off(self, screen, viz_note):
        self.viz_manager.remove_unit(viz_note.note, id(viz_note))


class PresetMultiTrackChordsCircle(BasePreset):
    """
    Like multi-track chords, except with chords displayed in a circle-of-fifths pattern, with the song's key at the top of the circle.
    """
    def __init__(self, vn, name, desc):
        super().__init__(vn, name, desc)
        self.circle_origin = 0, 0
        self.circle_radius = 0
        self.current_chord_unit = None
        self.chord_particle_unit = None

    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.num_tracks = len(score.parts)
        display_size = self.viz_manager.main_frame.display.size
        x = display_size.x // 2
        y = display_size.y // 2

        # draw the three circles
        circle_unit_outer = unit.CircleUnit(x, y, 210, 2, (255, 255, 255))
        circle_unit_outer.layer = 1
        circle_unit_middle = unit.CircleUnit(x, y, 140, 2, (255, 255, 255))
        circle_unit_middle.layer = 1
        circle_unit_inner = unit.CircleUnit(x, y, 70, 2, (255, 255, 255))
        circle_unit_inner.layer = 1
        self.viz_manager.units.append(circle_unit_outer)
        self.viz_manager.units.append(circle_unit_middle)
        self.viz_manager.units.append(circle_unit_inner)

        self.circle_origin = circle_unit_outer.x, circle_unit_outer.y
        self.circle_radius = 210

        # draw the 12 lines that separate the circle into 12 quadrants
        for i in range(0, 12):
            x_inner = circle_unit_outer.x + (circle_unit_inner.radius * math.cos(math.radians(-90 + (30 * i) + (0.5 * 30))))
            y_inner = circle_unit_outer.y + (circle_unit_inner.radius * math.sin(math.radians(-90 + (30 * i) + (0.5 * 30))))
            x_outer = circle_unit_outer.x + (circle_unit_outer.radius * math.cos(math.radians(-90 + (30 * i) + (0.5 * 30))))
            y_outer = circle_unit_outer.y + (circle_unit_outer.radius * math.sin(math.radians(-90 + (30 * i) + (0.5 * 30))))

            line_unit = unit.LineUnit(x_inner, y_inner, x_outer, y_outer, (255, 255, 255), 2)
            line_unit.layer = 1
            self.viz_manager.units.append(line_unit)

        self.viz_manager.sort_units()

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.scale_degree_to_color(note, self.viz_manager.key)
        track_width = screen_x // self.num_tracks

        h = screen_y // (self.highest_pitch - (self.lowest_pitch - 1))
        rect_note = unit.RectNoteUnit(0, 0, color, note, track_width, h)
        rect_note.id = id(viz_note)

        region_x = track_width * (viz_note.track - 1)
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y, True)

        rect_note = util.create_unit_in_center_of_quadrant(rect_note, (region_x, 0), (region_x + track_width, screen_y))
        rect_note.y = y

        self.viz_manager.units.append(rect_note)
        self.viz_manager.sort_units()
        self.notes_played.append(viz_note)

        # dissonance stuff
        dissonance = muse.get_dissonance_of_note(viz_note, self.viz_manager, self.notes_played)
        # print("dissonance: " + str(dissonance))
        rect_note.dissonance = dissonance

        # chord stuff
        recent_notes = muse.get_recent_notes(self.notes_played)
        chord = muse.get_chord(recent_notes)

        # quarter-note chords
        # chord = viz_note.chord_in_beat

        # half-bar chords
        # chord = viz_note.chord_in_half_bar

        # bar chords
        # chord = viz_note.chord_in_bar

        chord_name = chord.pitchedCommonName
        s1 = str(chord_name)
        s2 = ""
        if isinstance(self.latest_chord, music21.chord.Chord):
            s2 = str(self.latest_chord.pitchedCommonName)
        if s1 != s2:
            print("new chord: " + str(chord_name) + "\t(" + str(chord.quality) + ")")

            if self.latest_chord is None:
                self.latest_chord = chord

            self.latest_chord = chord
            root = self.latest_chord.root()
            note = music21.note.Note(root)
            quality = self.latest_chord.quality

            color = colorhelper.scale_degree_to_color(note, self.viz_manager.key)
            x, y = muse.get_pos_on_circle_of_fifths(note, self.circle_origin, self.circle_radius, self.viz_manager.key, quality)

            particle_unit = unit.ParticleSpaceUnit(screen, x // 2, y // 2, screen_x, screen_y, color)

            if self.current_chord_unit is not None:
                self.current_chord_unit.remove_particles()
                # self.viz_manager.remove_unit(note, self.current_chord_unit.id, the_type)

            self.viz_manager.units.append(particle_unit)

            self.current_chord_unit = particle_unit

            # circle_chord = unit.CircleNoteUnit(x, y, color, note, 20)
            # circle_chord.id = id(note)
#
            # the_type = type(circle_chord)
#
            # if self.current_chord_unit is not None:
            #     self.viz_manager.remove_unit(note, self.current_chord_unit.id, the_type)

            # self.viz_manager.units.append(circle_chord)
            # self.current_chord_unit = circle_chord

    def per_note_off(self, screen, viz_note):
        self.viz_manager.remove_unit(viz_note.note, id(viz_note))


class PresetTensionCornell(BasePreset):
    """

    """
    def first_load(self, score):
        self.key = score.analyze('key')         # uses the Krumhansl-Schmuckler key determination algorithm
        self.num_tracks = len(score.parts)
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, viz_note):
        self.notes_played.append(viz_note)
        tension = muse.get_sequential_tension(viz_note, self.notes_played, self.key)
        # print("Tension: {0} from note {1} in track {2}".format(tension, viz_note.note.name, viz_note.track))
        screen.fill((tension, tension, tension))
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        color = colorhelper.simple_note_to_color_tuple(note)
        r = 15
        circle_note = unit.CircleNoteUnit(0, 0, color, note, r)

        interval = screen_x // self.num_tracks

        # Add white line down center of the screen
        for i in range(0, screen_x, interval):
            line = unit.LineUnit(i, 0, i, screen_y, (255, 255, 255), 1)
            self.viz_manager.units.append(line)

        x = interval * (viz_note.track - 1)
        circle_note = util.create_unit_in_center_of_quadrant(circle_note, (0, 0), ((x + interval), screen_y))
        circle_note.y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        self.viz_manager.units.append(circle_note)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetChordRoot(BasePreset):
    """
    This preset aims to detect chords being played and displays the root note of each chord.
    It also draws a piano roll visualization of the notes, just like normal piano roll.
    """
    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

    def per_note_on(self, screen, message):
        self.notes_played.append(message)
        recent_notes = muse.get_recent_notes(self.notes_played)
        chord = muse.get_chord(recent_notes)
        chord_name = chord.pitchedCommonName
        # dbg = self.viz_manager.main_frame.debugger.textbox
        s1 = str(chord_name)
        s2 = ""
        if isinstance(self.latest_chord, music21.chord.Chord):
            s2 = str(self.latest_chord.pitchedCommonName)
        if s1 != s2:
            print("new chord: " + str(chord_name))
            # util.print_line_to_panel(dbg, "new chord: " + str(chord_name) + "\n")

            screen_x = self.viz_manager.main_frame.display.size.x
            screen_y = self.viz_manager.main_frame.display.size.y

            if self.latest_chord is None:
                self.latest_chord = chord

            root = self.latest_chord.root()
            note = music21.note.Note(root)
            self.viz_manager.remove_unit(note)

            self.latest_chord = chord
            root = self.latest_chord.root()
            note = music21.note.Note(root)

            color = colorhelper.simple_note_to_color_tuple(note)
            rect_note = unit.RectNoteUnit(300, 0, color, note, 200, 60)
            rect_note.h = 60
            rect_note = util.create_unit_in_center_of_quadrant(rect_note, (0, 0), (screen_x, screen_y))
            rect_note.y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)

            self.viz_manager.units.append(rect_note)

        else:
            pass
            # util.print_line_to_panel(dbg, "------")

    def per_note_off(self, screen, message):
        pass


class PresetInstrumentGroups(BasePreset):
    """
    Similar to the multitrack preset except notes belonging to an instrument group are assigned its own shape.
        Strings - triangle
        Brass - circle
        Woodwind - ellipse
        Keyboards - square
        Percussion - rhombus
        Other (i.e. sound effects) - circle (not filled)
    """
    def first_load(self, score):
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)
        self.num_tracks = len(score.parts)

    def per_note_on(self, screen, viz_note):
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

        # Add track divider lines
        col_wid = screen_x // self.num_tracks
        for i in range(0, screen_x, col_wid):
            line = unit.LineUnit(i, 0, i, screen_y, (255, 255, 255), 1)
            self.viz_manager.units.append(line)

        color = colorhelper.simple_note_to_color_tuple(note)
        vn = None
        y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        x_interval = col_wid * (viz_note.track - 1)
        x = (x_interval * 2 + col_wid) // 2
        offset = 0

        instr_midi = self.viz_manager.instrument_map[viz_note.track-1]
        strings = list(range(25, 52, 1))
        brass = list(range(57, 64)) + [65, 66, 67, 68, 70]
        woodwind = list(range(73, 80)) + [69, 71, 72]
        keyboards = list(range(24))
        percussion = list(range(113, 120)) + [48]

        # Determine shape
        if instr_midi in strings:
            offset = 7
            vn = unit.TriangleNoteUnit(x, y, color, note, 30, 0)
        elif instr_midi in brass:
            offset = 15
            vn = unit.CircleNoteUnit(x, y, color, note, 15)
        elif instr_midi in woodwind:
            offset = 30
            vn = unit.EllipseNoteUnit(x, y, color, note, 60, 30, 0)
        elif instr_midi in keyboards:
            offset = 30
            vn = unit.RectNoteUnit(x, y, color, note, 30, 30)
        elif instr_midi in percussion:
            offset = 60
            vn = unit.DiamondNoteUnit(x, y, color, note, 60, 0)
        else:
            offset = 15
            vn = unit.EllipseNoteUnit(x, y, color, note, 30, 30, 1)

        vn.x -= offset
        self.viz_manager.units.append(vn)

    def per_note_off(self, screen, message):
        self.viz_manager.remove_unit(message.note)


class PresetJulien(BasePreset):
    """

    """
    def first_load(self, score):
        self.key = score.analyze('key')                 # uses the Krumhansl-Schmuckler key determination algorithm
        self.num_tracks = len(score.parts)
        self.lowest_pitch, self.highest_pitch = util.get_edge_pitches(score)

        # Add track divider lines
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y
        col_wid = screen_x // self.num_tracks
        for i in range(0, screen_x, col_wid):
            line = unit.LineUnit(i, 0, i, screen_y, (255, 255, 255), 1)
            self.viz_manager.units.append(line)

    def per_note_on(self, screen, viz_note):
        self.notes_played.append(viz_note)
        note = viz_note.note
        screen_x = self.viz_manager.main_frame.display.size.x
        screen_y = self.viz_manager.main_frame.display.size.y

        # Create red rectangle of tension
        tension = muse.get_sequential_tension(viz_note, self.notes_played, self.key)
        alpha = tension + 40
        if alpha > 215:
            alpha = 215
        mid_x = screen_x // 3
        mid_y = screen_y // 3
        color = colorhelper.change_color_brightness((30, 0, 0), tension)
        rect = unit.RectNoteUnit(mid_x, mid_y, color, None, mid_x, mid_y)

        # Adds tension rect to background (i.e. everything else is drawn on top)
        rect.layer = 1
        self.viz_manager.units.append(rect)
        self.viz_manager.sort_units()
        # self.notes_played.append(viz_note)

        col_wid = screen_x // self.num_tracks

        # use note's dissonance to determine color brightness brightness
        color2 = colorhelper.simple_note_to_color_tuple(note)
        dissonance = muse.get_dissonance_of_note(viz_note, self.viz_manager, self.notes_played)
        color3 = colorhelper.change_color_brightness(color2, -dissonance)

        note_y = util.graph_note_y(note, self.highest_pitch, self.lowest_pitch, screen_y)
        x_interval = col_wid * (viz_note.track - 1)
        note_x = (x_interval * 2 + col_wid) // 2

        # List of instrument groups and instruments in them
        strings = list(range(25, 52, 1))
        brass = list(range(57, 64)) + [65, 66, 67, 68, 70]
        woodwind = list(range(73, 80)) + [69, 71, 72]
        keyboards = list(range(24))
        percussion = list(range(113, 120)) + [48]

        # Determine shape from instrument group
        instr_midi = self.viz_manager.instrument_map[viz_note.track - 1]
        if instr_midi in strings:
            offset = 7
            vn = unit.TriangleNoteUnit(note_x, note_y, color3, note, 30, 0)
        elif instr_midi in brass:
            offset = 15
            vn = unit.CircleNoteUnit(note_x, note_y, color3, note, 15)
        elif instr_midi in woodwind:
            offset = 30
            vn = unit.EllipseNoteUnit(note_x, note_y, color3, note, 60, 30, 0)
        elif instr_midi in keyboards:
            offset = 30
            vn = unit.RectNoteUnit(note_x, note_y, color3, note, 30, 30)
        elif instr_midi in percussion:
            offset = 60
            vn = unit.DiamondNoteUnit(note_x, note_y, color3, note, 60, 0)
        else:
            offset = 15
            vn = unit.EllipseNoteUnit(note_x, note_y, color3, note, 30, 30, 1)
        vn.SetFade(True, 8, True)

        vn.x -= offset
        self.viz_manager.units.append(vn)

        # draws rectangles on sides representing the root of the last chord played
        self.notes_played.append(viz_note)
        recent_notes = muse.get_recent_notes(self.notes_played)
        chord = muse.get_chord(recent_notes)
        chord_name = chord.pitchedCommonName
        s1 = str(chord_name)
        s2 = ""
        if isinstance(self.latest_chord, music21.chord.Chord):
            s2 = str(self.latest_chord.pitchedCommonName)
        if s1 != s2:
            if self.latest_chord is None:
                self.latest_chord = chord

            root = self.latest_chord.root()
            note = music21.note.Note(root)
            self.viz_manager.remove_unit(note, id(note), type(unit.RectChordUnit))

            self.latest_chord = chord
            root = self.latest_chord.root()
            note = music21.note.Note(root)

            color = colorhelper.scale_degree_to_color(note, self.viz_manager.key)
            rect_chord = unit.RectChordUnit(0, 0, color, note, screen_x, screen_y, 20)
            rect_chord.id = id(note)

            self.viz_manager.units.append(rect_chord)


class PresetParticles(BasePreset):
    """

    """
    def first_load(self, score):
        w, h = self.viz_manager.main_frame.display.size
        particles = unit.ParticleSpaceUnit(self.viz_manager.screen, 0, 0, w, h, (100, 123, 87), self.viz_manager)
        self.viz_manager.units.append(particles)
        pass

    def per_note_on(self, screen, viz_note):
        # h, w = self.viz_manager.main_frame.display.size
        # particles = unit.ParticleSpaceUnit(self.viz_manager.screen, 0, 0, h, w, (100, 123, 87), self.viz_manager)
        # self.viz_manager.units.append(particles)
        pass
