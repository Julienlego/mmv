#!/usr/bin/env python
"""
Dialog to browse and select a preset to load to the system.
"""
import wx


class PresetDialog(wx.Frame):

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
