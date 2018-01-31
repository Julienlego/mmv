#!/usr/bin/env python

import pygame, wx, os, sys
import src.VizManager as vm

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSize()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.resized = False


    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))

        pygame.draw.circle(self.screen, (0, 255, 0), (250, 250), 125)

        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

    def OnSize(self, event):
        self.size = self.GetSizeTuple()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)


class DebugFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, title='Debug', size=(300,250))
        self.parent = parent
        pan = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Create debug text box
        self.textbox = wx.TextCtrl(pan, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer.Add(self.textbox, 0, flag=wx.EXPAND, border=2)
        pan.SetSizer(sizer)

class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent, size):
        super(MainFrame, self).__init__(parent, title="Midi Music Visualizer", size=size)

        # Create the panels
        topPanel = wx.Panel(self, size=(800, 600))
        panelPygame = wx.Panel(topPanel, -1, pos=(0,100), size=(800,600))
        panelDebug = wx.Panel(topPanel, -1, pos=(100,0), size=(250,250))

        self.display = PygameDisplay(self, -1)
        self.display.SetSize((800, 520))
        self.vizmanager = vm.VizManager(self.display.screen)

        self.SetMinSize((300, 200))  # the frame starts looking weird if it gets too small

        # Create menu bar
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        viewmenu = wx.Menu()

        self.fileopen = filemenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        self.runviz = filemenu.Append(wx.ID_ANY, 'Run', 'Run Viz')
        self.toggledebug = viewmenu.Append(wx.ID_ANY, 'Show Debugger', 'Toggle debug box', kind=wx.ITEM_CHECK)
        viewmenu.Check(self.toggledebug.GetId(), True)

        # Create status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("No file selected", 0)
        self.statusbar.SetStatusText("No preset selected", 1)

        menubar.Append(filemenu, '&File')
        menubar.Append(viewmenu, '&View')

        # Bind everything!
        self.Bind(wx.EVT_MENU, self.OnQuit)
        self.Bind(wx.EVT_MENU, self.OpenFile, self.fileopen)
        self.Bind(wx.EVT_MENU, self.PlayVisualization, self.runviz)
        self.Bind(wx.EVT_MENU, self.ToggleDebugBox, self.toggledebug)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Add panels to sizer and set to panel
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panelPygame, 0, flag=wx.EXPAND|wx.ALL, border=10)
        sizer.Add(panelDebug, 1, flag=wx.EXPAND|wx.ALL, border=10)

        self.child = DebugFrame(self)
        self.child.Show()

        self.SetMenuBar(menubar)
        self.SetAutoLayout(True)
        topPanel.SetSizerAndFit(sizer)
        self.Centre()
        self.Show(True)

    def OnQuit(self, event):
        """
        Called when the exit
        """
        self.display.Kill(event)
        pygame.quit()
        self.Close()
        self.Destroy()

    def OnSize(self, event):
        """
        Called whenever the main frame is re-sized
        """
        #self.display.SetSize(event.GetSize())
        #print("Size: ", self.display.size)
        self.display.SetSize(event.GetSize() - (0, 85))  # magic number for now
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

    def ToggleDebugBox(self, event):
        """
        Shows/Hides the debug textbox
        """
        if self.toggledebug.IsChecked():
            if self.child:
                self.child.Show()
            else:
                self.child = DebugFrame(self)
                self.child.Show()
        else:
            if self.child:
                self.child.Hide()

    def PlayVisualization(self, event):
        """
        Plays the whatever preset and song are currently loaded.
        """
        self.vizmanager.Play()

    def PauseVisualization(self, event):
        """
        Pauses whatever visualization is running, if any.
        """
        pass

class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, size=(800, 600))
        self.frame.Show()
        self.SetTopWindow(self.frame)

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
