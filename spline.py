import itertools
import logging, datetime
import pickle
import sys
from enum import Enum
from typing import List

import numpy as np
import pyglet
from pyglet.window import mouse, key

from Vector import Vector2
from selectable import SelectableList

logger = logging.getLogger(__name__)
date = datetime.datetime.now().strftime("%y.%m.%d-%H:%M")
logging.basicConfig(filename=f"{date}.log", level=logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
stream_formatter = logging.Formatter("%(levelname)s: %(message)s")
sh.setFormatter(stream_formatter)
logger.addHandler(sh)


class Global:
    u"""We don't like global variables, right? store theme here"""
    SELECTABLE_MODS = SelectableList()  # store here all selectable objects


class InputMap:
    u"""Input map."""

    def __init__(self):
        self.move = InputMap.ActorControl()
        self.game = InputMap.GameControl()

    class ActorControl:
        top = key.UP
        down = key.DOWN
        left = key.LEFT
        right = key.RIGHT

    class Selection:
        u"""Select spline or select point in spline."""
        next_ = key.Q
        previous = key.E
        switch_selectable = key.TAB  # switch between different types of selections

    class GameControl:
        restart = key.R  # clean and start again
        exit = key.ESCAPE
        mod_switch = key.SPACE  # switch window mods
        enter = key.ENTER  # used for drawing
        speed_up = key.NUM_ADD  # change speed of moving points
        speed_down = key.NUM_SUBTRACT  # like above


class SplineException(Exception):
    def __init__(self):
        super(SplineException, self).__init__()
        logger.exception("Could not initialize spline! Not enough points given.")


class Spline:
    u"""Class for mathematics behind splines."""

    def __init__(self, points=List[Vector2]):
        self.points = SelectableList(points)
        if len(self.points) < 4:
            raise SplineException
        self._selected_point = self.points.value

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


class SplineWindowModes(Enum):
    u"""Enumerate possible modes for SplineWindow class."""
    set_points = 0  # Pressing mouse provide selecting points on a screen
    idle = 1  # Ignore user input until switch to other mode
    select_point = 2  # Select one of existing points


# noinspection PyAbstractClass
class SplineWindow(pyglet.window.Window):
    u"""Main window for spline application"""
    modes = itertools.cycle(SplineWindowModes)

    default_file = "splines.pickled"

    def __init__(self, *args, **kwargs):
        super(SplineWindow, self).__init__(**kwargs)
        self.mode: SplineWindowModes = next(SplineWindow.modes)
        logger.debug(self.mode)
        self.splines: SelectableList[Spline] = SelectableList()
        self.selected_spline = self.splines.selected_index

        # going to _SELECTABLES_MODS
        Global.SELECTABLE_MODS.append(self.splines)

        self._tmp = {"points": []}  # dict for handling any temporary data
        self._iterate_splines = iter(self.splines)

        self.selected_points = None
        self._spline_resolution = 0.005

        self.batch = pyglet.shapes.Batch()
        self._drawings = []

        self.input_map = InputMap()
        self._SELECTED_ITEM = Global.SELECTABLE_MODS.next_item()

        if "test" in args:
            self._test_sample = [Vector2(x, y) for (x, y) in
                                 [(102, 233), (248, 131), (458, 176), (510, 367), (316, 417)]]
            self.add_spline(self._test_sample)
            self.draw_spline(0)

    def draw_splines(self):
        u"""Draw all saved splines."""
        for index in range(len(self.splines)):
            self.draw_spline(index)

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
        Global.SELECTABLE_MODS.append(spline.points)
        self._tmp["points"].clear()

        logger.debug(Global.SELECTABLE_MODS)

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
        # WINDOW
        if symbol == key.SPACE:
            self.mode = next(SplineWindow.modes)
            logger.debug(f"Current mode is: {self.mode}")
        elif symbol == key.ESCAPE:
            logger.info("Bye bye!")
            sys.exit(pyglet.app.exit())

        # EXPORT AND LOAD
        elif symbol == key.X:
            self.export_spline(self.selected_spline)
        elif symbol == key.Z:
            self.load_saved_spline(SplineWindow.default_file)

        # Drawings
        elif symbol == key.ENTER:
            self.draw_spline()
        elif symbol == key.ENTER and modifiers == key.MOD_SHIFT:
            logger.debug("Pressed: ENTER")
            self.draw_splines()

        # SELECTION
        elif symbol == self.input_map.Selection.switch_selectable:
            self._SELECTED_ITEM = Global.SELECTABLE_MODS.next_item()
            logger.debug(self._SELECTED_ITEM)
        elif symbol == self.input_map.Selection.next_:
            current = self._SELECTED_ITEM.next_item()
            logger.debug(current)
        elif symbol == self.input_map.Selection.previous:
            current = self._SELECTED_ITEM.previous_item()
            logger.debug(current)

    def export_spline(self, index=0):
        u"""Export spline to file."""
        with open(SplineWindow.default_file, "wb") as fb:
            pickle.dump(self.splines[index], fb)
        logger.info("Successfully exported splines to pickle object!")

    def load_saved_spline(self, file):
        u"""Load pickled spline"""
        try:
            with open(file, 'rb') as fb:
                spline = pickle.load(fb)
                self.splines.append(spline)
        except FileNotFoundError:
            logger.exception(f"Could not find following file: {file}")

        logger.info("Successfully loaded pickled spline.")


def main():
    window = SplineWindow(resizable=True)
    logger.info("Creating window.")

    pyglet.app.run()


if __name__ == '__main__':
    main()
