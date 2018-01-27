#!/usr/bin/env pythonx

import pygame
import wx
import src.VizManager as vm
import os

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSizeTuple()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))

        cur = 0

        while cur <= self.size[1]:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, self.size[1] - cur), (cur, 0))

            cur += self.linespacing

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

class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent):
        super(MainFrame, self).__init__(parent, title="Midi Music Visualizer", size=(800, 600))
        panel = wx.Panel(self)
        self.InitUI(panel)
        self.vizmanager = vm.VizManager()
        self.Centre()
        self.Show(True)

    def InitUI(self, panel):
        """
        Setup the main frame with all the panels, file menu, and status bar
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.display = PygameDisplay(self, -1)

        # Create menu bar
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        fileopen = filemenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        filequit = filemenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)

        # Create debug text box
        self.debugbox = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)

        # Bind events
        self.Bind(wx.EVT_MENU, self.OnQuit, filequit)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileopen)

        # Add panels to sizer and set to panel
        sizer.Add(self.display, 0, flag=wx.EXPAND|wx.ALL, border=2)
        sizer.Add(self.debugbox, 1, flag=wx.EXPAND|wx.ALL, border=2)
        panel.SetSizerAndFit(sizer)

    def OnQuit(self, e):
        self.Destroy()

    def OnSize(self):
        self.Layout()

    def OnOpen(self, e):
        self.Open()

    def Open(self):
        """
        Opens a file explorer to select a midi file and loads it into the viz manager
        """
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            self.vizmanager.LoadSongFromPath(dialog.GetPath())  # send the file to midi parser

        dialog.Destroy()

    def OnDraw(self):
        pass

    def Update(self, event):
        pass


class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show()
        self.SetTopWindow(self.frame)

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
