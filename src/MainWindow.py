#!/usr/bin/env pythonx

# simple.py

import pygame
import wx
from wx import glcanvas
import src.VizManager as vm
import src.MidiParser as mp
import src.GraphicsSystem as gs
import os
import math

CONST_WINDOW_TITLE = "Midi Music Visualizer"
CONST_WINDOW_WIDTH = 800
CONST_WINDOW_HEIGHT = 600


class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        os.environ['SDL_VIDEODRIVER"'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSize()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0, 0, 0))



        pygame.display.update()

    def OnPaint(self, event):
        self.Redraw()

    def OnSize(self, event):
        self.size = self.GetSize()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)

        self.display = PygameDisplay(self, -1)

        self.InitUI()

        # Viz manager object.
        self.viz_manager = vm.VizManager()
        self.midi_parser = mp.MidiParser()
        self.graphics_system = gs.GraphicsSystem(self.display)

        # self.statusbar = self.CreateStatusBar()
        # self.statusbar.SetFieldsCount(3)
        # self.statusbar.SetStatusWidths([-3, -4, -2])
        # self.statusbar.SetStatusText("wxPython", 0)
        # self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

        self.curframe = 0

        self.SetTitle("Pygame embedded in wxPython")

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.timer.Start((1000.0 / self.display.fps))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.display, 1, flag=wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileOpen = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        fileQuit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen)

        self.SetSize((800, 600))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)

    def Kill(self, event):
        self.display.Kill(event)
        pygame.quit()
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def Update(self, event):
        self.curframe += 1

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        self.Open()

    # opens a file explorer
    def Open(self):
        wildcard = "MIDI file (*.mid)|"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            self.midi_parser.parse_file(dialog.GetPath())  # send the file to midi parser

        dialog.Destroy()


class MainFrame(wx.Frame):
    """
    This class is the main window class.
    All of the setup is done in the init function.
    """

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.InitUI()

        # Viz manager object.
        self.viz_manager = vm.VizManager()
        self.midi_parser = mp.MidiParser()
        self.graphics_system = gs.GraphicsSystem()

        # Set up pygame in wx window
        screen = pygame.display.set_mode((800, 600))

        # Draw a circle
        # self.make_circle(25, 100)

        # make the button here???
        # app = wx.App()

        # frame = wx.Frame(None, -1, 'Sample Text')
        # frame.Show()

        # app.MainLoop()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileOpen = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open a file')
        fileQuit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuit)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen)

        self.SetSize((800, 600))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        self.Open()

    # opens a file explorer
    def Open(self):
        wildcard = "MIDI file (*.mid)|"  # only .mid files
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            print(dialog.GetPath())
            self.midi_parser.parse_file(dialog.GetPath())  # send the file to midi parser

        dialog.Destroy()

    # BUTTON TEST
    def onButton(event):
        print("button pressed")

    """
    def make_circle(self, num_points, radius):
        verts = []
        for i in range(num_points):
            angle = math.radians(float(i) / num_points * 360.0)
            x = radius * math.cos(angle) + 300
            y = radius * math.sin(angle) + 200
            verts += [x,y]
        global circle
        circle = pyglet.graphics.vertex_list(num_points, ('v2f', verts))
    """

    def on_draw(self):
        """
        Called by pyglet to draw the canvas.

        window.clear()
        label = pyglet.text.Label('HELLO WORLD!!!',
                          font_size=42,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
        label.draw()

        global circle
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        #pyglet.gl.glColor3f(0,10,0)
        circle.draw(pyglet.gl.GL_LINE_LOOP)
        """
        pass

    def update(self):
        """
        Called repeatedly by the pyglet clock.

        Main loop.

        """

    def on_key_press(self, symbol, modifiers):
        """
        Called when the end user modifies a key that was pressed.

        :param symbol: int
            Number representing the key that was pressed
        :param modifiers: int
            Number representing any modified keys that were pressed

        """
        pass

    def on_key_release(self, symbol, modifiers):
        """
        Called when the end user releases a key.

        :param symbol: int
            Number representing the key that was pressed.
        :param modifiers: int
            Number representing any modifying keys that were pressed.

        """
        pass


class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)

        return True


def main():
    app = App()
    # app = wx.App()
    # MainFrame(None, title='Sample Text')
    app.MainLoop()


if __name__ == '__main__':
    main()
