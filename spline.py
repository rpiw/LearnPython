from typing import List

import pyglet
from pyglet.window import mouse, key
import logging
import numpy as np
from enum import Enum
import itertools
import sys
from Vector import Vector2

logger = logging.getLogger(__name__)


class SplineException(Exception):
    def __init__(self):
        super(SplineException, self).__init__()
        logger.exception("Could not initialize spline! Not enough points given.")


class Spline:
    u"""Class for mathematics behind splines."""
    def __init__(self, points=List[Vector2]):
        self.points = points
        if len(self.points) < 4:
            raise SplineException
        self._selected_point = 0

    def __repr__(self):
        return f"Spline: length {len(self.points)},: from: {self.points[0] if self.points else None}"

    def get_spline_point(self, t: float = 0.5, loop=True) -> Vector2:
        # not loop does not work: FIX ME
        if not loop:
            p1 = int(t.__floor__()) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
        else:
            p1 = int(t)
            p2 = (p1 + 1) % len(self.points)
            p3 = (p2 + 1) % len(self.points)
            p0 = p1 - 1 if p1 >= 1 else len(self.points) - 1

        t = t - int(t)

        tt = t ** 2
        ttt = t ** 3

        q1 = -ttt + 2 * tt - t
        q2 = 3 * ttt - 5 * tt + 2
        q3 = -3 * ttt + 4 * tt + t
        q4 = ttt - tt

        x = 0.5 * (self.points[p0].x * q1 + self.points[p1].x * q2 + self.points[p2].x * q3 + self.points[p3].x * q4)
        y = 0.5 * (self.points[p0].y * q1 + self.points[p1].y * q2 + self.points[p2].y * q3 + self.points[p3].y * q4)

        return Vector2(x, y)

    def next_point(self):
        self._selected_point += 1
        if self._selected_point == len(self.points):
            self._selected_point = 0
        return self.points[self._selected_point]

    def previous_points(self):
        self._selected_point -= 1
        if self._selected_point < 0:
            self._selected_point = len(self.points) - 1
        return self.points[self._selected_point]


class SplineWindowModes(Enum):
    u"""Enumerate possible modes for SplineWindow class."""
    idle = 0  # Ignore user input until switch to other mode
    set_points = 1  # Pressing mouse provide selecting points on a screen
    select_point = 2  # Select one of existing points


# noinspection PyAbstractClass
class SplineWindow(pyglet.window.Window):
    u"""Main window for spline application"""
    modes = itertools.cycle(SplineWindowModes)

    def __init__(self, *args, **kwargs):
        super(SplineWindow, self).__init__(**kwargs)
        self.mode: SplineWindowModes = next(SplineWindow.modes)
        self.mode = next(SplineWindow.modes)  # begin with set_points mode
        self.splines: List[Spline] = []
        self.selected_spline = 0

        self._tmp = {"points": []}  # dict for handling any temporary data
        self._iterate_splines = iter(self.splines)

        self.selected_points = None
        self._spline_resolution = 0.005

        self.batch = pyglet.shapes.Batch()
        self._drawings = []

        if "test" in args:
            self._test_sample = [Vector2(x, y) for (x, y) in [(102, 233), (248, 131), (458, 176), (510, 367), (316, 417)]]
            self.add_spline(self._test_sample)
            self.draw_spline(0)

    def draw_spline(self, index: int = 0):
        u"""Draw splines of index index in self.splines."""
        for t in np.arange(0, len(self.splines[index].points) - self._spline_resolution, self._spline_resolution):
            point = self.splines[index].get_spline_point(t)
            figure = pyglet.shapes.Rectangle(point.x - 1, point.y - 1, 3, 3, color=(255, 255, 255), batch=self.batch)
            self._drawings.append(figure)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def add_spline(self, list_of_points=None):
        if list_of_points is None:
            list_of_points = self._tmp["points"]
        # noinspection PyTypeChecker
        spline = Spline(list_of_points.copy())
        self.splines.append(spline)
        print(f"Splines {self.splines}")
        self._tmp["points"].clear()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.mode is SplineWindowModes.idle:
            return
        elif self.mode is SplineWindowModes.set_points:
            if button == mouse.LEFT:
                self._tmp["points"].append(Vector2(x, y))  # collect samples
            elif button == mouse.RIGHT:
                self.add_spline()  # put samples to Spline and clear cache

        elif self.mode is SplineWindowModes.select_point:
            logger.debug("on_mouse_press: self.mode is SplineWindowModes.select_point -- NOT IMPLEMENTED.")

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.mode = next(SplineWindow.modes)
            print(f"Current mode is: {self.mode}")
        elif symbol == key.ESCAPE:
            logger.info("Bye bye!")
            sys.exit(pyglet.app.exit())
        elif symbol == key.X:
            pass
        elif symbol == key.Y:
            pass
        elif symbol == key.ENTER:
            self.draw_spline(self.selected_spline)

    def selected_point_next(self):
        # self.selected_points =
        pass


def main():
    window = SplineWindow("test", resizable=True)
    logger.info("Creating window.")

    pyglet.app.run()


if __name__ == '__main__':
    main()
