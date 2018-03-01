#!/usr/bin/env python
import src.Preset as pr
import src.MidiParser as mp
import wx
import pygame
import pygame.midi
import src.Utilities as util


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

        # the tempo of the song
        self.tempo = 0

        # the start time of the song, in ticks
        self.start_time = 0

        # bool for if the song is playing
        self.isPlaying = False

        # bool for if the song should play
        self.should_play = False

        # the list of units to draw to the screen
        self.units = []

        # the list of notes in the currently open file, one after the other with chords broken down
        self.notes = []

        # the list of the currently playing notes
        # it is a list of tuples. first value is note, second is the tick it was played on
        self.current_notes = []

        # the list of the next notes to be played (more than 1 if they occur simultaneously)
        # it is a list of tuples. first value is note, second is the tick it should play on
        self.next_notes = []

        # the offset of the last note in the song
        self.last_offset = 0.

        # the midi player
        pygame.midi.init()
        self.player = pygame.midi.Output(0)

        # Init and load all presets
        self.LoadPresets()

    def LoadPresets(self):
        """
        Create and loads all presets.
        """
        # Create the preset!
        # simple_circle = pr.PresetSimpleCircle(self, "Default", "This is a default visualization preset.")
        piano_roll = pr.PresetPianoRoll(self, "Piano-Roll", "This is a basic piano roll preset. The height of the note is determined by its pitch.")
        piano_static = pr.StaticPianoRollPreset(self, "Piano-Roll Static", "This is a static preset that draws the entire song onto the screen in a piano-roll fashion.")
        piano_rading = pr.PresetPianoRollFading(self, "Fading Piano-Roll", "Similar to the Piano-Roll preset, but the notes fade over time.")
        piano_roll_color = pr.PresetColorPianoRoll(self, "Color Piano Roll", "This preset is the same as the piano roll preset except it determines the color by the note.")
        multi_piano = pr.TwoTrackPianoRoll(self, "Two-track Piano Roll", "This is similar to .")


        # Add the preset to the dictionary!
        # self.presets.update({simple_circle.name: simple_circle})
        self.presets.update({piano_roll_color.name: piano_roll_color})
        self.presets.update({piano_roll.name: piano_roll})
        self.presets.update({piano_static.name: piano_static})
        self.presets.update({multi_piano.name: multi_piano})

    def LoadPreset(self, key):
        """
        Load preset with given key.
        """
        self.preset = self.presets[key]

    def LoadSongFromPath(self, path):
        """
        Reads file at given path, if possible, and saves as an object.
        """
        bsy = wx.BusyInfo("Loading song from path: " + path)
        self.parser.ParseFile(path)
        self.units.clear()
        self.tempo = self.parser.GetTempo()
        self.main_frame.statusbar.SetStatusText("Tempo: " + str(self.tempo) + " bpm", 2)
        bsy = None

    def Play(self):
        """
        Starts playing the visualization from the beginning.
        """
        bsy = wx.BusyInfo("Initial Loading...")
        self.preset.OnFirstLoad(self.parser.score)
        bsy = None
        dbg = self.main_frame.debugger.textbox

        part = self.parser.score.parts[0]   # Gets first track/part of song

        # Prints all notes/rests in part to debug panel
        util.PrintLineToPanel(dbg, "Note/Rest\tOctave\tLen\tOffset\n")
        self.main_frame.debugger.WriteLine("Note/Rest\tOctave\tLen\tOffset\n")


        self.notes = util.GetNotesList(self.parser.score)
        # Iterates through all notes, rests, and chords

        # for n in notes:
        #     if isinstance(n, note.Note):
        #         util.PrintNoteToPanel(dbg, n)
        #         self.notes.append(n)
        #
        #     elif isinstance(n, note.Rest):
        #         util.PrintRestToPanel(dbg, n)
        #
        #     elif isinstance(n, chord.Chord):
        #         util.PrintChordToPanel(dbg, n)
        #         chord_notes = n._notes
        #         for chord_note in chord_notes:
        #             if isinstance(chord_note, note.Note):
        #                 new_note = chord_note
        #                 new_note.offset = n.offset
        #                 new_note.quarterLength = n.quarterLength
        #                 self.notes.append(new_note)

        for n in self.notes:
            util.PrintNoteToPanel(dbg, n.note)

        util.PrintLineToPanel(dbg, "\n\n===============================")


        self.should_play = True
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


                oq_error = 0
                qlq_error = 0
                try:
                    oq_error = n.note.editorial.offsetQuantizationError
                    mts += oq_error
                except AttributeError:
                    pass

                new_next_note.append(ticks + mts)
                self.next_notes.append(new_next_note)
            if n.note.offset > self.last_offset:
                self.last_offset = n.note.offset

    def Pause(self):
        """
        Stops the visualization at wherever it is.
        """
        pass

    def Update(self):
        """

        """
        if not self.isPlaying:
            if self.should_play:
                self.should_play = False
                self.isPlaying = True
                self.start_time = pygame.time.get_ticks()
            return
        # determine whether or not to play something
        ticks = pygame.time.get_ticks()

        # see if any current notes are done playing and must be set to off
        # then remove them from current_notes
        for n in self.current_notes:
            if len(n) > 1:
                if ticks >= n[1]:
                    self.player.note_off(n[0].note.pitch.midi, n[0].note.volume.velocity)
                    self.preset.PerNoteOff(self.screen, n[0])
                    self.current_notes.remove(n)

        if self.next_notes != None:
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

                                    new_next_note.append(ticks + util.OffsetMS((m.note.offset - current_offset), self.tempo) + util.OffsetMS(oq_error, self.tempo))
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
                        self.player.note_on(n[0].note.pitch.midi, n[0].note.volume.velocity)
                        self.preset.PerNoteOn(self.screen, n[0])



    def remove_unit(self, note):
        """
        Removes whichever units in the units list that are associated with that note.
        :param note: the note with which to match to a unit
        :return: none
        """
        for unit in self.units:
            if unit.note == note:
                self.units.remove(unit)
                # print("unit removed. list size: " + str(len(self.units)))
