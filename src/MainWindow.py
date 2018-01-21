#!/usr/bin/env pythonx

# simple.py

import pyglet
import math
import wx
import src.VizManager as vm

CONST_WINDOW_TITLE = "Midi Music Visualizer"
CONST_WINDOW_WIDTH = 800
CONST_WINDOW_HEIGHT = 600


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

        # Draw a circle
        #self.make_circle(25, 100)

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

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        self.Open()

    def Open(self):
        print("opening")


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


def main():
    app = wx.App()
    MainFrame(None, title='Sample Text')
    app.MainLoop()


if __name__ == '__main__':
    main()
