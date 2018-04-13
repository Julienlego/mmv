#!/usr/bin/env python
"""

"""
import wx
from util.Constants import INSTRUMENTS


class InstrumentFrame(wx.Frame):
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
            choices = list(INSTRUMENTS.keys())
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
                midi_val = INSTRUMENTS[box.Items[box.GetSelection()]]
            i = self.combo_boxes.index(box)
            self.parent.vizmanager.instrument_map[i] = midi_val
        self.OnClose(event)

    def OnClose(self, event):
        self.Close()
        self.Destroy()
