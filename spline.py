import pyglet
from pyglet.window import mouse, key
import logging
import numpy as np
from enum import Enum


logger = logging.getLogger(__name__)


class Spline:
    u"""Class for mathematics behind splines."""


class SplineWindowModes(Enum):
    u"""Enumerate possible modes for SplineWindow class."""
    idle = 0  # Ignore user input until switch to other mode
    set_points = 1  # Pressing mouse provide selecting points on a screen
    select_point = 2  # Select one of existing points


# noinspection PyAbstractClass
class SplineWindow(pyglet.window.Window):
    u"""Main window for spline application"""
    mode: SplineWindowModes = SplineWindowModes.idle

    def __init__(self, *args, **kwargs):
        super(SplineWindow, self).__init__(**kwargs)

    def on_draw(self):
        self.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"Pressed mouse button: {x}, {y}.")


def main():
    window = SplineWindow(resizable=True)
    logger.info("Creating window.")

    pyglet.app.run()


if __name__ == '__main__':
    main()
