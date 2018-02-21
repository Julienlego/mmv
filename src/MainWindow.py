#!/usr/bin/env python

import pygame, wx, os, sys
import src.VizManager as vm
import src.Unit as Unit

frame = None

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSizeTuple()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.viz_manager = None

        self.resized = False
        self.is_fullscreen = False

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)


    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))

        for unit in self.viz_manager.units:
            if isinstance(unit, Unit.NoteRect):
                if unit.should_delete:
                    self.viz_manager.units.remove(unit)
                else:
                    unit.update()
                    unit.draw(self.screen)

        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.size.width/2), int(self.size.height/2)), 100)

        self.viz_manager.main_frame.statusbar.SetStatusText("t: " + str(pygame.time.get_ticks()), 3)

        self.viz_manager.Update()

        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

    def OnSize(self, event):
        self.size = self.GetSizeTuple()

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
        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)


class DebugFrame(wx.Frame):
    """
    Debug frame with textbox to display info relevant to the preset.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, title=title, size=(300, 400))
        self.parent = parent
        self.SetMinSize((250, 400))
        self.SetMaxSize((300, 400))
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
        wx.Dialog.__init__(self, parent, title=title, size=(500, 250))
        self.lst_presets = presets
        self.parent = parent
        wx.StaticText(self, -1, 'Select a preset to load', (20, 20))
        self.lst = wx.ListBox(self, pos=(20, 50), size=(150, -1), choices=presets, style=wx.LB_SINGLE | wx.TE_MULTILINE)
        self.text = wx.StaticText(self, wx.ID_ANY, pos=(200, 50), size=(270, -1), label="No description.", style=wx.TE_MULTILINE | wx.TE_READONLY)
        btn = wx.Button(self, 1, 'Select', (70, 150), style=wx.Center)
        btn.SetFocus()

        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.lst)
        self.Bind(wx.EVT_BUTTON, self.OnSelect)

    def GetNameSelect(self, event):
        preset = self.lst.GetSelection()  # gets int pos of preset
        return self.lst_presets[preset]

    def OnListBox(self, event):
        """
        What to do when a preset is highlighted.
        """
        name = self.GetNameSelect(self)
        desc = self.parent.vizmanager.presets[name].desc
        self.text.SetLabel(desc)

    def OnSelect(self, event):
        """
        Loads selected preset to the vizmanager and writes name to statusbar.
        """
        name = self.GetNameSelect(self)
        print("Preset selected: ", name)
        self.parent.statusbar.SetStatusText(name, 1)
        self.parent.vizmanager.LoadPreset(name)
        self.Destroy()

    def OnClose(self, event):
        self.Close()
        self.Destroy()


class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title=title, size=size)
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

        # Create menu items
        self.fileopen = filemenu.Append(wx.ID_OPEN, 'Open File\tCtrl+O', 'Open a file')
        self.runviz = filemenu.Append(wx.ID_ANY, 'Run\tCtrl+R', 'Run Viz')
        self.toggledebug = self.viewmenu.AppendCheckItem(wx.ID_ANY, 'Show Debugger\tCtrl+B', 'Toggle showing the debug box')
        self.ldp = self.viewmenu.Append(wx.ID_ANY, 'Load Preset\tCtrl+P')
        self.fullscreen = self.viewmenu.Append(wx.ID_ANY, "Fullscreen\tCtrl+F", "Fullscreen")

        # Create status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([-3, -4, -2, -2])
        self.statusbar.SetStatusText("No file selected", 0)
        self.statusbar.SetStatusText("No preset selected", 1)

        # Add file and menu options to menu bar
        menubar.Append(filemenu, '&File')
        menubar.Append(self.viewmenu, '&View')

        # Bind everything!
        self.Bind(wx.EVT_MENU, self.OnQuit)
        self.Bind(wx.EVT_MENU, self.OpenFile, self.fileopen)
        self.Bind(wx.EVT_MENU, self.PlayVisualization, self.runviz)
        self.Bind(wx.EVT_MENU, self.ToggleDebugBox, self.toggledebug)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.LoadPreset, self.ldp)
        self.Bind(wx.EVT_MENU, self.ToggleFullscreen, self.fullscreen)


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
        pygame.quit()
        self.Close()
        self.Destroy()

    def OnSize(self, event):
        """
        Called whenever the main frame is re-sized
        """
        self.Layout()

    def OpenFile(self, event):
        """
        Opens a file explorer to select a midi file and loads it
        """
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            self.statusbar.SetStatusText(dialog.GetPath(), 0)
            self.vizmanager.LoadSongFromPath(dialog.GetPath())

        dialog.Destroy()

    def LoadPreset(self, event):
        """
        Load selected preset from the submenu
        """
        frame = PresetDialog(self, "", list(self.vizmanager.presets.keys()))
        frame.Show(True)
        frame.Centre()

    def ToggleDebugBox(self, event):
        """
        Shows/Hides the debug textbox
        """
        if self.toggledebug.IsChecked():
            if self.debugger:
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggledebug.GetId(), True)
                self.debugger.Show()
            else:
                self.debugger = DebugFrame(self, "Debugger")
                self.debugger.isEnabled = True
                self.viewmenu.Check(self.toggledebug.GetId(), True)
                self.debugger.Show()
        else:
            if self.debugger:
                self.viewmenu.Check(self.toggledebug.GetId(), False)
                self.debugger.isEnabled = False
                self.debugger.Hide()

    def PlayVisualization(self, event):
        """
        Plays the whatever preset and song are currently loaded.
        """
        if self.vizmanager.preset is None:
            wx.MessageBox("No preset was selected", "Missing Preset!", wx.OK | wx.ICON_ERROR)
        elif self.vizmanager.parser.IsEmpty() is True:
            wx.MessageBox("No midi file was selected", "Missing File!", wx.OK | wx.ICON_ERROR)
        else:
            self.vizmanager.Play()

    def PauseVisualization(self, event):
        """
        Pauses whatever visualization is running, if any.
        """
        pass

    def OnButtonKeyEvent(self, event):
        keycode = event.GetKeyCode()
        print(keycode)

    def ToggleFullscreen(self, event):
        """

        """
        self.display.ToggleFullscreen(event)


class App(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Midi Music Visualizer", size=(800, 600))
        frame.Show()
        self.SetTopWindow(frame)

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
