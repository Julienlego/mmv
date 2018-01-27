#!/usr/bin/env python
import wx
import sys
import pygame

class GraphicsSystem:
    """
    This class will handle generating graphical effects.
    It will contain functions that will access the methods of
    the various graphics libraries we are using.
    """

    def __init__(self, display):
        self.screen = display.screen
        print("graphics system init")
        pygame.init()
        print(pygame.font.get_fonts())
        self.DrawText(100, 100, "sample text")

    def DrawText(self, x, y, text):
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(text, True, (255,0,0), (255,255,255))
        textrect = text.get_rect()
        textrect.centerx = self.screen.get_rect().centerx
        textrect.centery = self.screen.get_rect().centery
        self.screen.blit(text, textrect)
        pygame.display.flip()

