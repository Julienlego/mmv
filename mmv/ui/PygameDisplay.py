#!/usr/bin/env python
"""

"""
import wx, pygame, os, sys


class PygameDisplay(wx.Window):

    def __init__(self, parent, id):
        super().__init__(parent, id)
        self.parent = parent
        self.hwnd = self.GetHandle()
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSize()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.viz_manager = None

        self.resized = False
        self.is_fullscreen = False

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

    def update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation ui etc.)
        self.redraw()

    def redraw(self):
        self.screen.fill((0, 0, 0))

        for unit in self.viz_manager.units:
            # if isinstance(unit, Unit.RectNoteUnit):
            if unit.should_delete is True:
                self.viz_manager.units.remove(unit)
            else:
                unit.update()
                unit.draw(self.screen)

        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.size.width/2), int(self.size.height/2)), 100)

        self.viz_manager.main_frame.statusbar.SetStatusText("t: " + str(pygame.time.get_ticks()), 3)

        self.viz_manager.update()

        pygame.display.update()

    def on_paint(self, event):
        self.redraw()

    def on_size(self, event):
        # self.screen.fill((0, 0, 0))
        self.size = self.GetSize()

    def toggle_fullscreen(self, event):
        """

        """
        pass

    def kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.on_paint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.update, source=self.timer)
        pygame.quit()
