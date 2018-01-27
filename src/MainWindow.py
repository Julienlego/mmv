#!/usr/bin/env pythonx

# simple.py

import pygame, wx, os
import src.VizManager as vm
import src.MidiParser as mp


class PyGameDisplay(wx.Window):
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

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

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

    def __init__(self, parent, title, width, height):
        super(MainFrame, self).__init__(parent, title=title, size=(width, height))

        self.panel = wx.Panel(self)

        self.frame_width = width
        self.frame_height = height

        self.viz_manager = vm.VizManager(self.panel)

        #self.display = PyGameDisplay(self, -1)

        # Create menu bar
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        fileopen = filemenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        filequit = filemenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)

        # Bind events
        self.Bind(wx.EVT_MENU, self.OnQuit, filequit)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileopen)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # Create the sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.debugbox = wx.TextCtrl(panel,
                                    size=(self.frame_width/4, self.frame_height),
                                    style=wx.TE_MULTILINE|wx.TE_READONLY
                                    )

        #sizer.Add(self.display, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        sizer.Add(self.debugbox, 1, wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, 5)

        #self.SetAutoLayout(True)

        # Use the sizers to set the frame
        self.SetSizer(sizer)

        self.Layout()
        self.Center()
        self.Show()
        self.Fit()

    """
    Quits the frame
    
    """
    def OnQuit(self, e):
        self.display
        pygame.quit()

    """
    Opens a file explorer to select a .mid file
    
    """
    def OnOpen(self, e):
        wildcard = "MIDI file (*.mid)|*.mid"  # only .mid files

        # Create and show the open filedialog
        dialog = wx.FileDialog(None, message="Open MIDI file",
                               defaultDir=os.getcwd(),
                               defaultFile="",
                               wildcard=wildcard,
                               style=wx.ID_OPEN
                               )

        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            # send the file to midi parser
            self.viz_manager.LoadSong(dialog.GetPath())

        dialog.Destroy()

    def OnKeyTyped(self, event):
        print(event.GetString())

    def OnSize(self, event):
        self.Layout()

    def on_draw(self):
        pass

    def update(self):
        pass

"""
Main App for software.

"""
class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None,
                               title="Midi Music Visualizer",
                               width=800, height=600
                               )
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()
