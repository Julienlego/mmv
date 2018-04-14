#!/usr/bin/env python
"""
This class is the core window class.
All of the setup is done in the init function.
"""
import wx
import pygame
import sys
import os
import mmv.ui.DebugFrame as dbf
import mmv.ui.PygameDisplay as pyf
import mmv.ui.PresetDialog as prf
import mmv.core.VizManager as vm
import mmv.ui.InstrumentFrame as isf
import mmv.util.Utilities as util


class MainFrame(wx.Frame):

    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        self.SetMinSize((300, 200))  # the frame starts looking weird if it gets too small

        self.debugger = dbf.DebugFrame(self, "Debugger")
        self.display = pyf.PygameDisplay(self, -1)
        self.vizmanager = vm.VizManager(self, self.display.screen)

        # give the PygameDisplay access to the viz manager for drawing
        self.display.viz_manager = self.vizmanager

        # Create menu bar
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        self.viewmenu = wx.Menu()
        self.midimenu = wx.Menu()

        # Create menu items
        self.file_open = filemenu.Append(wx.ID_OPEN, 'Open File\tCtrl+O', 'Open a file')
        self.run_viz = filemenu.Append(wx.ID_ANY, 'Load Selected Preset\tCtrl+L', 'Play Viz')
        self.toggle_debug = self.viewmenu.AppendCheckItem(wx.ID_ANY, 'Show Debugger\tCtrl+B', 'Toggle showing the debug box')
        self.ldp = self.viewmenu.Append(wx.ID_ANY, 'Select Preset\tCtrl+P')
        self.fullscreen = self.viewmenu.Append(wx.ID_ANY, "Fullscreen\tCtrl+F", "Fullscreen")
        self.toggle_play = self.midimenu.Append(wx.ID_ANY, 'Play/Pause\tSpace', 'Play/Pause the visualization')
        self.select_tracks = self.midimenu.Append(wx.ID_ANY, 'Track Select\tCtrl+T', 'Select instruments for each track')
        self.print_songz = self.viewmenu.Append(wx.ID_ANY, 'Print Song', 'Print the currently loaded song to the debug panel')

        # Create status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(5)
        self.statusbar.SetStatusWidths([-100, -40, -20, -15, -25])
        self.statusbar.SetStatusText("No file selected", 0)
        self.statusbar.SetStatusText("No preset selected", 1)

        # Add file and menu options to menu bar
        menubar.Append(filemenu, '&File')
        menubar.Append(self.viewmenu, '&View')
        menubar.Append(self.midimenu, '&MIDI')

        # Bind everything!
        self.Bind(wx.EVT_MENU, self.on_quit)
        self.Bind(wx.EVT_MENU, self.load_file, self.file_open)
        self.Bind(wx.EVT_MENU, self.play_visualization, self.run_viz)
        self.Bind(wx.EVT_MENU, self.toggle_debugbox, self.toggle_debug)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.load_selected_preset, self.ldp)
        self.Bind(wx.EVT_MENU, self.toggle_fullscreen, self.fullscreen)
        self.Bind(wx.EVT_MENU, self.toggle_playing, self.toggle_play)
        self.Bind(wx.EVT_MENU, self.show_instrument_selector, self.select_tracks)
        self.Bind(wx.EVT_MENU, self.print_song, self.print_songz)

        # Add panels to sizer and set to panel
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.display, 1, flag=wx.EXPAND)

        self.SetMenuBar(menubar)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.Show(True)

    def on_quit(self, event):
        """
        Called when the program exits.
        """
        self.display.kill(event)
        self.Close()
        self.Destroy()
        pygame.quit()
        sys.exit()

    def OnSize(self, event):
        """
        Called whenever the core frame is re-sized
        """
        self.Layout()
        self.vizmanager.units.clear()

    def load_file(self, event):
        """
        Opens a file explorer to select a midi file and loads it to the vizmanager
        """
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            selection = dialog.GetPath()
            self.statusbar.SetStatusText(selection, 0)
            self.vizmanager.load_song_from_path(selection)

        dialog.Destroy()

    def load_selected_preset(self, event):
        """
        Load selected preset from the preset dialog.
        """
        frame = prf.PresetDialog(self, "Select a preset to load", list(self.vizmanager.presets.keys()))
        frame.Show(True)
        frame.Centre()

    def toggle_debugbox(self, event):
        """
        Shows/Hides the debug textbox
        """
        if self.toggle_debug.IsChecked():
            if self.debugger:
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggle_debug.GetId(), True)
                self.debugger.Show()
            else:
                self.debugger = dbf.DebugFrame(self, "Debugger")
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggle_debug.GetId(), True)
                self.debugger.Show()
        else:
            if self.debugger:
                self.viewmenu.Check(self.toggle_debug.GetId(), False)
                self.debugger.isEnabled = False
                self.debugger.Hide()

    def show_instrument_selector(self, event):
        """
        Open the track selector dialog box
        """
        frame = isf.InstrumentFrame(self, "Track Selector")
        frame.Show(True)
        frame.Center()

    def play_visualization(self, event):
        """
        Plays the whatever preset and song are currently loaded.
        """
        if self.vizmanager.preset is None:
            wx.MessageBox("No preset was selected", "Missing Preset!", wx.OK | wx.ICON_ERROR)
        elif self.vizmanager.parser.is_empty() is True:
            wx.MessageBox("No midi file was selected", "Missing File!", wx.OK | wx.ICON_ERROR)
        else:
            self.vizmanager.load_preset()

    def toggle_playing(self, event):
        """
        Toggles the is_playing attribute of the VizManager
        """
        if self.vizmanager.preset_loaded:
            self.vizmanager.is_playing = not self.vizmanager.is_playing
            if not self.vizmanager.is_playing:
                self.vizmanager.notes_off()
                self.statusbar.SetStatusText(str(self.vizmanager.preset.name + " [PAUSED]"), 1)
            else:
                self.vizmanager.notes_on()
                self.statusbar.SetStatusText(str(self.vizmanager.preset.name), 1)

    def print_song(self, event):
        """
        Prints the song to the debug box through vizmanager
        """
        dbg = self.debugger.textbox
        notes = self.vizmanager.notes

        if notes:

            # Prints all notes/rests in part to debug panel
            util.print_line_to_panel(dbg, "\nNote/Rest\tOctave\tLen\tOffset\n")
            for n in notes:
                util.print_note_to_panel(dbg, n.note)
            util.print_line_to_panel(dbg, "\n\n===============================")
        else:
            util.print_line_to_panel(dbg, "\nNo song loaded!\n")

    def pause_viz(self, event):
        """
        Pauses whatever visualization is running, if any.
        """
        pass

    def toggle_fullscreen(self, event):
        """
        Toggle fullscreen display
        """
        self.display.toggle_fullscreen(event)

    def clear_display(self):
        """
        Clears the pygame display.
        """
        self.vizmanager.units.clear()
        self.display.screen.fill((0, 0, 0))
