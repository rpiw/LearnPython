import pyglet
from pyglet import shapes
import sys
from pyglet.window import key, mouse
from typing import Tuple, List, Union
import numpy as np


class Direction:

    top = [-1, 0]
    down = [1, 0]
    left = [0, -1]
    right = [0, 1]


class Grid:

    def __init__(self, x_scale: int = 16, y_scale: int = 16, grid_size_x: int = 20, grid_size_y: int = 20,
                 anchor=""):
        u"""Create a virtual grid mapping x_scale, y_scale pixels to one field on a grid.
            :grid_size_x, grid_size_y are integers.
            :anchor, str, "middle" - (0, 0) is in a middle of a field."""
        self.scale = x_scale, y_scale
        self.grid_size = grid_size_x, grid_size_y
        self.anchor = np.array((0.5, 0.5)) if anchor == "middle" else np.array((0, 0))

    def world_to_grid(self, x: int, y: int) -> Tuple[int, int]:
        u"""Return position on grid based on world coordinates."""
        new_x = x // self.scale[0] % self.grid_size[0]
        new_y = y // self.scale[1] % self.grid_size[1]

        return new_x, new_y

    def grid_to_world(self, x: int, y: int) -> Tuple[int, int]:
        u"""Return position in world based on grid coordinates. Returning coordinates are in anchor."""
        new_x = x * self.scale[0]
        new_y = y * self.scale[1]

        return new_x, new_y


class Snake:
    u"""Class representing snake itself. It does not provide 'game' related utilities, like
    collision detection!"""
    def __init__(self, position: Union[List[Tuple[int]], np.array]):
        u"""Position: list of tuples of int pairs indicating position of all fragments of body."""
        self.position = np.array(position, dtype=int)
        self.length = len(self.position)

    def move(self, new_position: List[int]):
        u"""Move head to position new_position. Rest body follows previous elements."""
        assert len(new_position) == 2
        pos = np.array([(new_position[0], new_position[1])], dtype=int)
        self.position = np.concatenate((pos, self.position[:-1]))

    def move_incremental(self, direction: Direction):
        u"""Move the snake for one field only."""
        head_current_position = self.position[0]
        new_head_position = head_current_position + direction
        self.move(new_head_position)

    def grow(self, new_head_position: List[int]):
        u"""Grow after moving rest of a body."""
        assert len(new_head_position) == 2
        last_part = self.position[-1]
        self.move(new_head_position)
        self.position = np.concatenate((np.array(last_part), self.position))
        self.length += 1

    def __str__(self):
        return f"Snake of length {self.length} with head on position: {self.position[0]}"

    def __repr__(self):
        return "Snake: " + str(self.position)


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

    class GameControl:
        restart = key.R
        exit = key.ESCAPE
        stop = key.SPACE
        start = key.ENTER
        speed_up = key.NUM_ADD
        speed_down = key.NUM_SUBTRACT


class Game:

    def __init__(self, w=640, h=480, speed=1, input_map=InputMap()):
        self.window = pyglet.window.Window(height=h, width=w)
        self.speed = speed
        self.input_map = input_map

    def main(self):

        batch = pyglet.shapes.Batch()

        square = shapes.Rectangle(200, 200, 200, 200, color=(100, 100, 100), batch=batch)

        @self.window.event
        def on_draw():
            self.window.clear()
            batch.draw()

        pyglet.app.run()


if __name__ == '__main__':
    game = Game()
    game.main()