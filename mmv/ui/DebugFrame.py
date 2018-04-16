#!/usr/bin/env python
"""
    Debug frame with textbox to display info relevant to the preset.
"""
import wx


class DebugFrame(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 400))
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

    def write_lane(self, line):
        """
        Writes line to the text-box.
        """
        self.textbox.AppendText(str(line))

    def on_close(self):
        self.parent.viewmenu.Check(self.parent.toggledebug.GetId(), False)
        self.Close()
        self.Destroy()
