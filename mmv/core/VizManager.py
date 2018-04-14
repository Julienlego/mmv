#!/usr/bin/env python
import wx
import pygame
import pygame.midi
import mmv.core.Unit as Unit
import util.Utilities as util
import mmv.midi.Player as play
import mmv.core.Preset as pr
import mmv.midi.MidiParser as mp
import random


class VizManager:
    """
    This class manages the entire visualization system, including
    midi parsing and all the presets.
    """

    def __init__(self, main_frame, screen):
        # Preset that is currently loaded
        self.preset = None
        # Stores all presets
        self.presets = {}
        # Pygame screen object of the display
        self.screen = screen
        self.main_frame = main_frame
        # Current frame of the visualization
        self.curr_frame = None  # 0, if a song or preset is loaded
        # Midi file parser. This contains the actual file path and musc21 score.
        self.parser = mp.MidiParser()
        # the midi player
        self.player = play.Player()

        # the tempo of the song
        self.tempo = 0

        # the start time of the song, in ticks
        self.start_time = 0

        # bool for if the song is playing
        self.is_playing = False

        # bool for if the song should play
        self.should_play = False

        # bool for if a preset is loaded
        self.preset_loaded = False

        # the list of units to draw to the screen
        self.units = []

        # the list of notes in the currently open file, one after the other with chords broken down
        self.notes = []

        # a dictionary mapping each track to its proper instrument
        self.instrument_map = [0 for x in range(16)]

        # the list of the currently playing notes
        # it is a list of tuples. first value is note, second is the tick it was played on
        self.current_notes = []

        # the list of the next notes to be played (more than 1 if they occur simultaneously)
        # it is a list of tuples. first value is note, second is the tick it should play on
        self.next_notes = []

        # the next id to be used by a unit
        self.next_id = 0

        # the key of the currently loaded song. set to 'C major' by default by the MidiParser.
        self.key = None

        # the offset of the last note in the song
        self.last_offset = 0.

        # dictionary of active particle effects. this exists because deleting units with particle effects in them
        # deletes the particles immediately, and sometimes we want a smooth ending to the effects
        self.particle_effects = {}

        self.initialize()

        random.seed()

    def initialize(self):
        """
        Runs when vizmanager is initialized
        """
        self.load_presets()

    def load_presets(self):
        """
        Create and loads all presets.
        """
        # Create the preset!
        text = "Similar to the Piano Roll Preset, except with a colored circle. Color is determined by the " \
               "note, and the height is relative to the lowest and highest note in the song. The radius is derived" \
               "from note's velocity."
        preset_simple_circle = pr.PresetSimpleColorCircleRelative(self, "Simple Colored Circles", text)

        text = "This is a basic piano roll preset. The height of the note is relative to the lowest and highest" \
               "pitch in the song."
        preset_piano_roll = pr.PresetPianoRoll(self, "Piano Roll", text)

        text = "This is a static preset that draws the entire song onto the screen in a piano-roll fashion."
        preset_piano_static = pr.PresetStaticPianoRoll(self, "Piano Roll Static", text)

        text = "Similar to the Piano-Roll preset, but the notes fade over time."
        preset_piano_fading = pr.PresetPianoRollFading(self, "Fading Piano Roll", text)

        text = "This preset is the same as the piano roll preset except it determines the color by the note."
        preset_piano_roll_color = pr.PresetColorPianoRoll(self, "Color Piano Roll", text)

        text = "Takes the first two tracks in the midi file and draws their notes in their part of the screen. Left" \
               "side is track 1, right side for track 2. The notes are drawn similarly to the Color Piano Roll preset."
        preset_two_track_piano = pr.PresetTwoTrackColorPianoRoll(self, "Two-track Piano Roll", text)

        text = "Piano roll with chord roots emphasized."
        preset_chord_root = pr.PresetChordRoot(self, "Chord Root", text)

        text = "Similar to Piano-Roll preset, but in black-white monochrome."
        preset_piano_roll_monochrome = pr.PresetMonochromePianoRoll(self, "Piano-Roll Monochrome", text)

        text = "Similar to the Simple Colored Circles, except the height is relative to the lowest and highest " \
               "possible midi pitches."
        preset_circle_max_pitch = pr.PresetSimpleColorCircleMaxPitch(self, "Color Piano Roll 2", text)

        text = "For each track, draw its current note as a colored circle in its own column region on the screen," \
               "where the leftmost column represents the 1st track, the next column to the right is the 2nd track," \
               "and so on."
        preset_multitrack_circle_piano = pr.PresetMultiTrackColorCircle(self, "Multi-track Colored Circles", text)

        text = "Similar to Two-track Piano Roll, except each track has its own column, starting with the leftmost" \
               "column representing the 1st track."
        preset_multitrack_piano_roll = pr.PresetMultiTrackColorPianoRoll(self, "Multi-track Colored Piano Roll", text)

        text = "Similar to the multi-track presets, except this uses the theories from the Cornell paper to depict " \
               "tonal tension as a grey-ish background hue."
        preset_tension_circle_color = pr.PresetTensionCornell(self, "Tension Colored Circles", text)

        text = "An extension of the Multi-Track Color Piano Roll, that adds visualization of chords being played"
        preset_multitrack_chords = pr.PresetMultiTrackChords(self, "Multi-track Chords", text)

        text = "Similar to the Multi-track Chords preset, with the chords shown in a circle-of-fifths style"
        preset_multitrack_chords_circle = pr.PresetMultiTrackChordsCircle(self, "Multi-track Chords Circle", text)

        text = "Similar to the multi-track presets, except the shape of the notes are determined by what instrument" \
               "group the instrument playing the note belongs to. Strings are triangles; Brass are circles; Woodwind" \
               "are are ellipses; Keyboards are square; Percussions are diamond. Anything else are unfilled circles."
        preset_instrumentgroup = pr.PresetInstrumentGroups(self, "Instrument Groups", text)

        text = "Combines the presets Instrument Group, Tension, and Chord Roots. Notes fade after they play."
        preset_complex = pr.PresetJulien(self, "Instruments, Tension, and Chord Roots", text)

        text = "Currently tests particle generator within a preset."
        preset_particles = pr.PresetParticles(self, "Particles", text)

        # Add the preset to the dictionary!
        self.presets.update({preset_piano_roll.name: preset_piano_roll})
        self.presets.update({preset_piano_static.name: preset_piano_static})
        self.presets.update({preset_piano_fading.name: preset_piano_fading})
        self.presets.update({preset_two_track_piano.name: preset_two_track_piano})
        self.presets.update({preset_simple_circle.name: preset_simple_circle})
        self.presets.update({preset_circle_max_pitch.name: preset_circle_max_pitch})
        self.presets.update({preset_piano_roll_color.name: preset_piano_roll_color})
        self.presets.update({preset_chord_root.name: preset_chord_root})
        self.presets.update({preset_piano_roll_monochrome.name: preset_piano_roll_monochrome})
        self.presets.update({preset_multitrack_circle_piano.name: preset_multitrack_circle_piano})
        self.presets.update({preset_multitrack_piano_roll.name: preset_multitrack_piano_roll})
        self.presets.update({preset_tension_circle_color.name: preset_tension_circle_color})
        self.presets.update({preset_multitrack_chords.name: preset_multitrack_chords})
        self.presets.update({preset_instrumentgroup.name: preset_instrumentgroup})
        self.presets.update({preset_multitrack_chords_circle.name: preset_multitrack_chords_circle})
        self.presets.update({preset_complex.name: preset_complex})
        self.presets.update({preset_particles.name: preset_particles})

    def set_preset(self, key):
        """
        Load preset with given key.
        """
        self.preset = self.presets[key]

    def load_song_from_path(self, path):
        """
        Reads file at given path, if possible, and saves as an object.
        """
        bsy = wx.BusyInfo("Loading song from path: " + path)

        # cleanup everything
        self.current_notes.clear()
        self.next_notes.clear()
        self.is_playing = False
        self.should_play = False
        self.preset_loaded = False

        # parse file
        self.parser.parse_file(path)
        self.instrument_map = self.parser.instruments
        self.units.clear()
        self.tempo = self.parser.get_tempo()
        self.notes = util.get_viz_notes(self.parser.score)
        self.key = util.analyze_key(self.parser.score)
        self.main_frame.statusbar.SetStatusText("Key: " + str(self.key), 4)

        # Print track instruments to debugger

        self.main_frame.statusbar.SetStatusText("Tempo: " + str(self.tempo) + " bpm", 2)
        bsy = None

    def load_preset(self):
        """
        Loads the currently selected preset. Calls its on_first_load function.
        """
        # clears all current units
        self.units.clear()
        self.screen.fill((0, 0, 0))

        bsy = wx.BusyInfo("Initial Loading...")
        self.preset.first_load(self.parser.score)
        bsy = None
        dbg = self.main_frame.debugger.textbox

        # part = self.parser.score.parts[0]   # Gets first track/part of song

        self.should_play = False
        self.next_notes = []

        # get the offset of the first note in the song
        # so we can put it in next_notes
        first_offset = self.notes[0].note.offset
        for n in self.notes:
            if n.note.offset == first_offset:
                ticks = pygame.time.get_ticks()
                new_next_note = [n]
                # new_next_note.append(ticks + util.offet_ms(n.offset, self.tempo))
                try:
                    mts = n.notes.midiTickStart
                except AttributeError:
                    mts = util.offet_ms(n.note.offset, self.tempo)
                try:
                    oq_error = n.note.editorial.offsetQuantizationError
                    mts += oq_error
                except AttributeError:
                    pass

                new_next_note.append(ticks + mts)
                self.next_notes.append(new_next_note)

            if n.note.offset > self.last_offset:
                self.last_offset = n.note.offset

        self.preset_loaded = True
        print("Preset Loaded")
        util.print_line_to_panel(dbg, "\nPreset Loaded\n\n")

    def pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def update(self):
        """

        """
        if not self.is_playing:
            if self.should_play:
                self.should_play = False
                self.is_playing = True
                self.start_time = pygame.time.get_ticks()
            return
        # determine whether or not to play something
        ticks = pygame.time.get_ticks()

        # see if any current notes are done playing and must be set to off
        # then remove them from current_notes
        for n in self.current_notes:
            if len(n) > 1:
                if ticks >= n[1]:
                    self.player.NoteOff(n[0].note.pitch.midi, n[0].note.volume.velocity)
                    self.preset.per_note_off(self.screen, n[0])
                    self.current_notes.remove(n)

        if self.next_notes is not None:
            if ticks >= self.next_notes[0][1]:
                # move next_notes to current_notes
                for n in self.next_notes:
                    new_current_note = [n[0]]
                    # new_current_note.append(None)
                    self.current_notes.append(new_current_note)
                self.next_notes.clear()

                # get the new next notes
                current_offset = self.current_notes[len(self.current_notes) - 1][0].note.offset
                if current_offset < self.last_offset:
                    for n in self.notes:
                        if n.note.offset > current_offset:
                            new_offset = n.note.offset
                            for m in self.notes:
                                if m.note.offset == new_offset:
                                    ticks = pygame.time.get_ticks()
                                    new_next_note = [m]

                                    oq_error = 0
                                    qlq_error = 0
                                    mts = 0
                                    try:
                                        oq_error = m.note.editorial.offsetQuantizationError
                                    except AttributeError:
                                        pass
                                    try:
                                        qlq_error = m.note.editorial.quarterLengthQuantizationError
                                    except AttributeError:
                                        pass
                                    try:
                                        mts = m.note.midiTickStart
                                    except AttributeError:
                                        pass

                                    offset = util.offet_ms((m.note.offset - current_offset), self.tempo) + \
                                             util.offet_ms(oq_error, self.tempo)
                                    new_next_note.append(ticks + offset)
                                    self.next_notes.append(new_next_note)
                            break

                # if we have reached the last note(s), set next_notes to none so we know not to keep checking for more
                else:
                    self.next_notes.clear()

                # set the ticks length of each current note and
                # play the note and draw it to the screen (via preset)
                for n in self.current_notes:
                    if len(n) < 2:
                        # print("note " + str(n[0].name) + " had no tick value set")
                        length = n[0].note.quarterLength

                        qlq_error = 0
                        try:
                            qlq_error = n[0].note.editorial.quarterLengthQuantizationError
                        except AttributeError:
                            pass
                        length_ms = util.offet_ms(length, self.tempo) + util.offet_ms(qlq_error, self.tempo)
                        n.append(ticks + length_ms)
                        track = n[0].track
                        # instrument = self.track_instrument_map[track - 1]
                        instrument = self.instrument_map[track - 1]
                        if instrument < 130:
                            if instrument > 0:
                                self.player.SetInstrument(instrument - 1)
                            else:
                                self.player.SetInstrument(instrument)
                            self.player.NoteOn(n[0].note.pitch.midi, n[0].note.volume.velocity)
                        else:       # if instrument is not 1-129
                            self.player.SetInstrument(20, 10)
                            self.player.NoteOn(n[0].note.pitch.midi, n[0].note.volume.velocity, channel=10)

                        self.preset.per_note_on(self.screen, n[0])

    def remove_unit(self, note=None, id=None, the_type=None):
        """
        Removes whichever units in the units list that are associated with that note.
        :param note: the note with which to match to a unit
        :return: none
        """
        for unit in self.units:
            # Check if unit is subclass of noteunit
            if issubclass(type(unit), Unit.NoteUnit):
                if id is not None:
                    if the_type is None:
                        if unit.id == id:
                            self.units.remove(unit)
                    else:
                        if unit.id == id and type(unit) == the_type:
                            self.units.remove(unit)
                elif unit.note == note:
                    if the_type is None:
                        self.units.remove(unit)
                    else:
                        if type(unit) == the_type:
                            self.units.remove(unit)
                    # print("unit removed. list size: " + str(len(self.units)))
            elif isinstance(unit, Unit.ParticleSpaceUnit):
                if unit.id == id:
                    self.units.remove(unit)

    def sort_units(self):
        self.units.sort(key=lambda x: x.layer)

    def notes_off(self):
        for note in self.current_notes:
            self.player.NoteOff(note[0].note.pitch.midi, note[0].note.volume.velocity)

    def notes_on(self):
        for note in self.current_notes:
            self.player.NoteOn(note[0].note.pitch.midi, note[0].note.volume.velocity)

    def get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id
