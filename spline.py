import pyglet
from pyglet.window import mouse, key
import logging
import numpy as np
from enum import Enum
import itertools
import sys


logger = logging.getLogger(__name__)


class Spline:
    u"""Class for mathematics behind splines."""
    def __init__(self, points=np.array([], dtype=int), interpolation="square"):
        self.points = points
        self.interpolation = interpolation

    def __repr__(self):
        return f"Spline: length {len(self.points)},: from: {self.points[0] if self.points else None}"


class SplineWindowModes(Enum):
    u"""Enumerate possible modes for SplineWindow class."""
    idle = 0  # Ignore user input until switch to other mode
    set_points = 1  # Pressing mouse provide selecting points on a screen
    select_point = 2  # Select one of existing points


# noinspection PyAbstractClass
class SplineWindow(pyglet.window.Window):
    u"""Main window for spline application"""
    modes = itertools.cycle(SplineWindowModes)

    def __init__(self, *args, mode=0, **kwargs):
        super(SplineWindow, self).__init__(**kwargs)
        self.mode: SplineWindowModes = next(SplineWindow.modes)
        self.splines = []
        self._tmp = {}  # dict for handling any temporary data

    def on_draw(self):
        self.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.mode is SplineWindowModes.idle:
            return
        elif self.mode is SplineWindowModes.set_points:
            if button == mouse.LEFT:
                try:
                    self._tmp["points"].append((x, y))
                except KeyError:
                    self._tmp["points"] = [(x, y)]
            elif button == mouse.RIGHT:
                try:
                    self.splines.append(Spline(self._tmp["points"]))
                    del self._tmp["points"]
                except KeyError:
                    pass
                print("Splines: {}".format(self.splines))

        elif self.mode is SplineWindowModes.select_point:
            logger.debug("on_mouse_press: self.mode is SplineWindowModes.select_point -- NOT IMPLEMENTED.")

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.mode = next(SplineWindow.modes)
            print(f"Current mode is: {self.mode}")
        elif symbol == key.ESCAPE:
            logger.info("Bye bye!")
            sys.exit(pyglet.app.exit())


def main():
    window = SplineWindow(resizable=True)
    logger.info("Creating window.")

    pyglet.app.run()


if __name__ == '__main__':
    main()
