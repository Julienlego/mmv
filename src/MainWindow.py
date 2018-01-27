#!/usr/bin/env pythonx

import pyglet
import math
import wx
import src.VizManager as vm
import src.MidiParser as mp
import os


class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent):
        super(MainFrame, self).__init__(parent, title="Midi Music Visualizer", size=(800, 600))
        panel = wx.Panel(self)
        self.InitUI(panel)
        self.vizmanager = vm.VizManager(panel)
        self.Centre()
        self.Show(True)

    def InitUI(self, panel):
        """
        Setup the main frame with all the panels, file menu, and status bar
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create menu bar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileOpen = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        fileQuit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Create debug text box
        debugbox = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)

        # Bind events
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen)

        # Add panels to sizer and set to panel
        sizer.Add(debugbox, 0, flag=wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, border=2)
        panel.SetSizerAndFit(sizer)

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        self.Open()

    # opens a file explorer
    def Open(self):
        """
        Opens a file explorer to select a midi file
        """
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            self.vizmanager.LoadSong(dialog.GetPath())  # send the file to midi parser

        dialog.Destroy()

    def on_draw(self):
        pass

    def update(self):
        pass


def main():
    app = wx.App()
    MainFrame(None)
    app.MainLoop()


if __name__ == '__main__':
    main()
