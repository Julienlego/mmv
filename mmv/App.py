#!/usr/bin/env python
"""

"""
import wx
from mmv.ui import MainFrame as mf


class App(wx.App):
    def OnInit(self):
        frame = mf.MainFrame(None, "Midi Music Visualizer", size=(1200, 800))
        frame.Show()
        self.SetTopWindow(frame)

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()