#!/usr/bin/env python

import pygame, wx, os, sys
import src.VizManager as vm
import src.Utilities as util


class PygameDisplay(wx.Window):
    """

    """
    def __init__(self, parent, id):
        super().__init__(parent, id)
        self.parent = parent
        self.hwnd = self.GetHandle()
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSize()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.viz_manager = None

        self.resized = False
        self.is_fullscreen = False

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

    def update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))

        for unit in self.viz_manager.units:
            # if isinstance(unit, Unit.RectNoteUnit):
            if unit.should_delete is True:
                self.viz_manager.units.remove(unit)
            else:
                unit.update()
                unit.draw(self.screen)

        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.size.width/2), int(self.size.height/2)), 100)

        self.viz_manager.main_frame.statusbar.SetStatusText("t: " + str(pygame.time.get_ticks()), 3)

        self.viz_manager.update()

        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

    def OnSize(self, event):
        # self.screen.fill((0, 0, 0))
        self.size = self.GetSize()

    def ToggleFullscreen(self, event):
        """

        """
        if self.is_fullscreen is False:
            pygame.display.set_mode((self.size.height, self.size.width), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.size)

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.update, source=self.timer)
        pygame.quit()


class DebugFrame(wx.Frame):
    """
    Debug frame with textbox to display info relevant to the preset.
    """
    def __init__(self, parent, title):
        super().__init__(None, title=title, size=(300, 400))
        self.parent = parent
        self.SetMinSize((300, 400))
        self.SetMaxSize((400, 600))
        self.isEnabled = False
        panel = wx.Panel(self)
        sizer = wx.BoxSizer()
        # Create debug text box
        self.textbox = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.textbox, proportion=1, flag=wx.EXPAND, border=2)
        panel.SetSizer(sizer)

    def WriteLine(self, line):
        """
        Writes line to the text-box.
        """
        self.textbox.AppendText(str(line))

    def OnDestroy(self):
        self.parent.viewmenu.Check(self.parent.toggledebug.GetId(), False)
        self.Close()
        self.Destroy()


class PresetDialog(wx.Dialog):
    """
    Dialog to browse and select a preset to load to the system.
    """
    def __init__(self, parent, title, presets):
        super().__init__(parent, title=title, size=(600, 250))
        self.lst_presets = presets
        self.parent = parent
        self.lst = wx.ListBox(self, pos=(10, 10), size=(250, 150), choices=self.lst_presets, style=wx.LB_SINGLE | wx.TE_MULTILINE)
        self.text = wx.TextCtrl(self,-1, pos=(270, 10), size=(300, 190), style=wx.TE_MULTILINE | wx.TE_READONLY)
        btn = wx.Button(self, 1, 'Select', (30, 175), style=wx.Center)
        btn.SetFocus()

        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.lst)
        self.Bind(wx.EVT_BUTTON, self.OnSelect)

    def GetNameSelect(self, event):
        """
        Returns the name of the currently selected preset
        """
        preset = self.lst.GetSelection()  # gets int pos of preset
        return self.lst_presets[preset]

    def OnListBox(self, event):
        """
        What to do when a preset is highlighted.
        """
        self.text.Clear()
        name = self.GetNameSelect(self)
        self.text.AppendText(self.parent.vizmanager.presets[name].desc)

    def OnSelect(self, event):
        """
        Loads selected preset to the vizmanager and writes name to statusbar.
        """
        name = self.GetNameSelect(self)
        print("Preset selected: ", name)
        self.parent.statusbar.SetStatusText(name, 1)
        self.parent.vizmanager.set_preset(name)
        self.OnClose(event)

    def OnClose(self, event):
        self.Close()
        self.Destroy()


class InstrumentFrame(wx.Dialog):
    """

    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 300))
        self.parent = parent
        tracks = list(self.parent.vizmanager.parser.score.parts)    # self.parent.vizmanager.tracks
        panel = wx.Panel(self, -1)
        self.text_labels = []
        self.combo_boxes = []

        for track in tracks:
            index = tracks.index(track)
            pos = (20 + ((index // 8) * 200), (25 * (index % 8)) + 10)
            text = wx.StaticText(panel, id=wx.ID_ANY, label="Track " + str(index + 1), pos=pos)
            self.text_labels.append(text)
            pos = 65 + ((index // 8) * 200), (25 * (index % 8)) + 8
            choices = list(util.instruments.keys())
            box = wx.ComboBox(panel, id=wx.ID_ANY, value="Default", pos=pos, size=(150, 20), choices=choices)
            self.combo_boxes.append(box)

        self.button = wx.Button(panel, id=wx.ID_ANY, label="Apply", pos=(200, 225), style=wx.CENTER)
        self.Bind(wx.EVT_BUTTON, self.LoadInstruments)

    def LoadInstruments(self, event):
        """
        Load what's selected to the vizmanager
        """
        for box in self.combo_boxes:
            midi_val = 1
            if box.GetSelection() >= 0:
                midi_val = util.instruments[box.Items[box.GetSelection()]]
            i = self.combo_boxes.index(box)
            self.parent.vizmanager.instrument_map[i] = midi_val
        self.OnClose(event)

    def OnClose(self, event):
        self.Close()
        self.Destroy()


class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent, title, size):
        super().__init__(parent, title=title, size=size)
        self.SetMinSize((300, 200))  # the frame starts looking weird if it gets too small

        self.debugger = DebugFrame(self, "Debugger")
        self.display = PygameDisplay(self, -1)
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
        self.run_viz = filemenu.Append(wx.ID_ANY, 'Play Selected Preset\tCtrl+R', 'Play Viz')
        self.toggle_debug = self.viewmenu.AppendCheckItem(wx.ID_ANY, 'Show Debugger\tCtrl+B', 'Toggle showing the debug box')
        self.ldp = self.viewmenu.Append(wx.ID_ANY, 'Select Preset\tCtrl+P')
        self.fullscreen = self.viewmenu.Append(wx.ID_ANY, "Fullscreen\tCtrl+F", "Fullscreen")
        self.toggle_play = self.midimenu.Append(wx.ID_ANY, 'Play/Pause\tSpace', 'Play/Pause the visualization')
        self.select_tracks = self.midimenu.Append(wx.ID_ANY, 'Track Select\tCtrl+T', 'Select instruments for each track')
        self.print_song = self.viewmenu.Append(wx.ID_ANY, 'Print Song', 'Print the currently loaded song to the debug panel')

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
        self.Bind(wx.EVT_MENU, self.OnQuit)
        self.Bind(wx.EVT_MENU, self.OpenFile, self.file_open)
        self.Bind(wx.EVT_MENU, self.PlayVisualization, self.run_viz)
        self.Bind(wx.EVT_MENU, self.ToggleDebugBox, self.toggle_debug)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.LoadSelectedPreset, self.ldp)
        self.Bind(wx.EVT_MENU, self.ToggleFullscreen, self.fullscreen)
        self.Bind(wx.EVT_MENU, self.TogglePlay, self.toggle_play)
        self.Bind(wx.EVT_MENU, self.ShowInstrumentSelector, self.select_tracks)
        self.Bind(wx.EVT_MENU, self.PrintSong, self.print_song)

        # Add panels to sizer and set to panel
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.display, 1, flag=wx.EXPAND)

        self.SetMenuBar(menubar)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.Show(True)

    def OnQuit(self, event):
        """
        Called when the program exits.
        """
        self.display.Kill(event)
        self.Close()
        self.Destroy()
        pygame.quit()
        sys.exit()

    def OnSize(self, event):
        """
        Called whenever the main frame is re-sized
        """
        self.Layout()
        self.vizmanager.units.clear()

    def OpenFile(self, event):
        """
        Opens a file explorer to select a midi file and loads it
        """
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            self.statusbar.SetStatusText(dialog.GetPath(), 0)
            self.vizmanager.load_song_from_path(dialog.GetPath())

        dialog.Destroy()

    def LoadSelectedPreset(self, event):
        """
        Load selected preset from the submenu
        """
        frame = PresetDialog(self, "Select a preset to load", list(self.vizmanager.presets.keys()))
        frame.Show(True)
        frame.Centre()

    def ToggleDebugBox(self, event):
        """
        Shows/Hides the debug textbox
        """
        if self.toggle_debug.IsChecked():
            if self.debugger:
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggle_debug.GetId(), True)
                self.debugger.Show()
            else:
                self.debugger = DebugFrame(self, "Debugger")
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggle_debug.GetId(), True)
                self.debugger.Show()
        else:
            if self.debugger:
                self.viewmenu.Check(self.toggle_debug.GetId(), False)
                self.debugger.isEnabled = False
                self.debugger.Hide()

    def ShowInstrumentSelector(self, event):
        """
        Open the track selector dialog box
        """
        frame = InstrumentFrame(self, "Track Selector")
        frame.Show(True)
        frame.Center()

    def PlayVisualization(self, event):
        """
        Plays the whatever preset and song are currently loaded.
        """
        if self.vizmanager.preset is None:
            wx.MessageBox("No preset was selected", "Missing Preset!", wx.OK | wx.ICON_ERROR)
        elif self.vizmanager.parser.is_empty() is True:
            wx.MessageBox("No midi file was selected", "Missing File!", wx.OK | wx.ICON_ERROR)
        else:
            self.vizmanager.play_preset()

    def TogglePlay(self, event):
        """
        Toggles the is_playing attribute of the VizManager
        """
        if self.vizmanager.preset_loaded:
            self.vizmanager.is_playing = not self.vizmanager.is_playing
            if not self.vizmanager.is_playing:
                self.statusbar.SetStatusText(str(self.vizmanager.preset.name + " [PAUSED]"), 1)
            else:
                self.statusbar.SetStatusText(str(self.vizmanager.preset.name), 1)

    def PrintSong(self, event):
        """
        Prints the song to the debug box through vizmanager
        """
        self.vizmanager.print_song()

    def PauseVisualization(self, event):
        """
        Pauses whatever visualization is running, if any.
        """
        pass

    def ToggleFullscreen(self, event):
        """
        Toggle fullscreen display
        """
        self.display.ToggleFullscreen(event)


class App(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Midi Music Visualizer", size=(1200, 800))
        frame.Show()
        self.SetTopWindow(frame)

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
