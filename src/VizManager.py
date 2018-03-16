#!/usr/bin/env python
import wx
import pygame
import pygame.midi
import src.Unit as Unit
import src.Utilities as util
import src.Player as play
import src.Preset as pr
import src.MidiParser as mp


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
        
        # the list of all tracks in the currently open file. each track contains all of its notes
        self.tracks = []

        # a dictionary mapping each track to its proper instrument
        self.track_instrument_map = {}

        # the list of the currently playing notes
        # it is a list of tuples. first value is note, second is the tick it was played on
        self.current_notes = []

        # the list of the next notes to be played (more than 1 if they occur simultaneously)
        # it is a list of tuples. first value is note, second is the tick it should play on
        self.next_notes = []

        # the offset of the last note in the song
        self.last_offset = 0.

        # Init and load all presets
        self.LoadPresets()

    def LoadPresets(self):
        """
        Create and loads all presets.
        """
        # Create the preset!
        text = "Similar to the Piano Roll Preset, except with a colored circle. Color is determined by the " \
               "note, and the height is relative to the lowest and highest note in the song. The radius is derived" \
               "from note's velocity."
        preset_simple_circle = pr.PresetSimpleColorCircleRelative(self, "Simple Colored Circles", text)

        # preset_grid_text = pr.PresetTest(self, "Just Text", "Draws a grid and text.")

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

        text = ""
        preset_multitrack_circle_piano = pr.PresetMultiTrackColorCircle(self, "Multitrack Colored Circles", text)

        text = ""
        preset_multitrack_color_piano_roll = pr.PresetMultiTrackColorPianoRoll(self, "Multitrack Colored Piano Roll", text)

        # Add the preset to the dictionary!
        self.presets.update({preset_piano_roll.name: preset_piano_roll})
        self.presets.update({preset_piano_static.name: preset_piano_static})
        self.presets.update({preset_piano_fading.name: preset_piano_fading})
        self.presets.update({preset_two_track_piano.name: preset_two_track_piano})
        self.presets.update({preset_simple_circle.name: preset_simple_circle})
        self.presets.update({preset_circle_max_pitch.name: preset_circle_max_pitch})
        self.presets.update({preset_piano_roll_color.name: preset_piano_roll_color})
        # self.presets.update({preset_grid_text.name: preset_grid_text})
        self.presets.update({preset_chord_root.name: preset_chord_root})
        self.presets.update({preset_piano_roll_monochrome.name: preset_piano_roll_monochrome})
        self.presets.update({preset_multitrack_circle_piano.name: preset_multitrack_circle_piano})
        self.presets.update({preset_multitrack_color_piano_roll.name: preset_multitrack_color_piano_roll})


    def SetPreset(self, key):
        """
        Load preset with given key.
        """
        self.preset = self.presets[key]
        # info = pygame.midi.get_device_info(0)
        # print(info)
        # self.player.NoteOn(39, 100, 9)

    def LoadSongFromPath(self, path):
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

        self.parser.ParseFile(path)
        self.units.clear()
        self.tempo = self.parser.GetTempo()
        self.notes, self.tracks = util.GetVizNotesAndTracks(self.parser.score)

        for track in self.tracks:
            self.track_instrument_map[self.tracks.index(track)] = 0

        self.main_frame.statusbar.SetStatusText("Tempo: " + str(self.tempo) + " bpm", 2)
        bsy = None

    def LoadPreset(self):
        """
        Starts playing the visualization from the beginning.
        """
        bsy = wx.BusyInfo("Initial Loading...")
        self.preset.OnFirstLoad(self.parser.score)
        bsy = None
        dbg = self.main_frame.debugger.textbox

        part = self.parser.score.parts[0]   # Gets first track/part of song

        self.should_play = False
        self.next_notes = []

        # get the offset of the first note in the song
        # so we can put it in next_notes
        first_offset = self.notes[0].note.offset
        for n in self.notes:
            if n.note.offset == first_offset:
                ticks = pygame.time.get_ticks()
                new_next_note = [n]
                # new_next_note.append(ticks + util.OffsetMS(n.offset, self.tempo))
                try:
                    mts = n.notes.midiTickStart
                except AttributeError:
                    mts = util.OffsetMS(n.note.offset, self.tempo)
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
        util.PrintLineToPanel(dbg, "Preset Loaded\n\n")

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def Update(self):
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
                    self.preset.PerNoteOff(self.screen, n[0])
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

                                    offset = util.OffsetMS((m.note.offset - current_offset), self.tempo) + \
                                             util.OffsetMS(oq_error, self.tempo)
                                    new_next_note.append(ticks + offset)
                                    self.next_notes.append(new_next_note)
                            break

                # if we have reached the last note(s), set next_notes to none so we know not to keep checking for more
                else:
                    self.next_notes = None

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
                        length_ms = util.OffsetMS(length, self.tempo) + util.OffsetMS(qlq_error, self.tempo)
                        n.append(ticks + length_ms)
                        instrument = self.track_instrument_map[n[0].track - 1]
                        if instrument < 128:
                            if instrument > 0:
                                self.player.SetInstrument(instrument - 1)
                            else:
                                self.player.SetInstrument(instrument)
                            self.player.NoteOn(n[0].note.pitch.midi, n[0].note.volume.velocity)
                        else:
                            self.player.SetInstrument(20, 10)
                            self.player.NoteOn(n[0].note.pitch.midi, n[0].note.volume.velocity, channel=10)
                        self.preset.PerNoteOn(self.screen, n[0])

    def remove_unit(self, note):
        """
        Removes whichever units in the units list that are associated with that note.
        :param note: the note with which to match to a unit
        :return: none
        """
        for unit in self.units:
            # Check if unit is subclass of noteunit
            if issubclass(type(unit), Unit.NoteUnit):
                if unit.note == note:
                    self.units.remove(unit)
                    # print("unit removed. list size: " + str(len(self.units)))

    def print_song(self):
        dbg = self.main_frame.debugger.textbox
        if self.notes:

            # Prints all notes/rests in part to debug panel
            util.PrintLineToPanel(dbg, "Note/Rest\tOctave\tLen\tOffset\n")
            for n in self.notes:
                util.PrintNoteToPanel(dbg, n.note)
            util.PrintLineToPanel(dbg, "\n\n===============================")
        else:
            util.PrintLineToPanel(dbg, "No song loaded!\n")

