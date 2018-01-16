#!/usr/bin/env python
import pyglet
import math
import src.VizManager as vm

CONST_WINDOW_TITLE = "Midi Music Visualizer"
CONST_WINDOW_WIDTH = 800
CONST_WINDOW_HEIGHT = 600

class MainFrame(pyglet.window.Window):
    """
    This class is the main window class.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

        # Viz manager object.
        self.viz_manager = vm.VizManager()

        # Draw a circle
        #self.make_circle(25, 100)

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
        self.clear()

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


if __name__ == "__main__":
   window = MainFrame(width=CONST_WINDOW_WIDTH, height=CONST_WINDOW_HEIGHT,
                      caption=CONST_WINDOW_TITLE)
   pyglet.app.run()
