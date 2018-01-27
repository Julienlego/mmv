#!/usr/bin/env python
import wx
import pyglet

class GraphicsSystem:
    """
    This class will handle generating graphical effects.
    It will contain functions that will access the methods of
    the various graphics libraries we are using.
    """

    def __init__(self):
        print("graphics system init")
        self.draw_square(100, 100, 200)

    def draw_square(self, x, y, width):
        pyglet.graphics.draw(4, pyglet.gl.GL_POINTS,
                             ('v2i', (10, 10, 30, 10, 10, 30, 30, 30))
                             )
