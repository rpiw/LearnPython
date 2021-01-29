import pyglet
from pyglet import shapes
from pyglet.window import key

from typing import List, Union

import numpy as np

from enum import Enum
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

import logging

logger = logging.getLogger(__name__)


class Vector2Exception(Exception):
    def __init__(self):
        super(Vector2Exception, self).__init__()
        logger.error(f"Can not initialize Vector2 with given arguments.")


class Vector2:
    u"""Class for 2-dimensional vectors in euclidean space."""
    def __init__(self, x, y=None):
        if y is None and isinstance(x, Sequence):
            if len(x) == 2:
                self.x = x[0]
                self.y = x[1]
        else:
            try:
                self.x = x
                self.y = y
            except Exception:
                raise Vector2Exception

    def dot(self, other) -> float:
        u"""Cartesian dot product."""
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        u"""Element-wise multiplication, not a dot product!"""
        return Vector2(self.x * other.x, self.y * other.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        sub = self - other
        if sub.x != 0 or sub.y != 0:
            return False
        return True

    def __setitem__(self, _key, value):
        if not isinstance(value, (int, float)):
            raise TypeError
        if _key == 0:
            self.x = value
        elif _key == 1:
            self.y = value
        else:
            raise IndexError

    def __getitem__(self, _key):
        if _key == 0:
            return self.x
        elif _key == 1:
            return self.y
        else:
            raise IndexError

    def __str__(self):
        return f"Vector2 x={self.x}, y={self.y}"

    def __repr__(self):
        return f"{self.x, self.y}"

    def __iter__(self):
        return iter((self.x, self.y))


class Direction:
    top = Vector2(0, 1)
    down = Vector2(0, -1)
    left = Vector2(-1, 0)
    right = Vector2(1, 0)


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


class Grid:

    def __init__(self, x_scale: int = 32, y_scale: int = 32, grid_size_x: int = 20, grid_size_y: int = 20,
                 anchor=""):
        u"""Create a virtual grid mapping x_scale, y_scale pixels to one field on a grid.
            :grid_size_x, grid_size_y are integers.
            :anchor, str, "middle" - (0, 0) is in a middle of a field,
            :wrap_borders, bool, if true, does not limit movement behind borders, but set to end -> beginning and
            beginning -> end."""
        self.scale = Vector2(x_scale, y_scale)
        self.size = Vector2(grid_size_x, grid_size_y)
        self.anchor = np.array((0.5, 0.5)) if anchor == "middle" else np.array((0, 0))

    def world_to_grid(self, position: Vector2) -> Vector2:
        u"""Return position on grid based on world coordinates."""
        new_x = position.x // self.scale[0] % self.size.x
        new_y = position.y // self.scale[1] % self.size.y

        return Vector2(new_x, new_y)

    def grid_to_world(self, position: Vector2) -> Vector2:
        u"""Return position in world based on grid coordinates. Returning coordinates are in anchor."""
        return position * self.scale


class Actor(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, position: Union[List[Vector2], np.array], player=True, input_map=InputMap()):
        self.input_map = input_map
        self.player = player
        self.position = np.array(position, dtype=int)

    @abstractmethod
    def __repr__(self):
        return f"Class<Actor>: player: {self.player}"

    @abstractmethod
    def move(self, new_position: Vector2):
        u"""Move player to a new position."""
        pass

    @abstractmethod
    def move_incremental(self, direction: Vector2):
        u"""Move player incrementally from current position."""
        pass


class Snake(Actor):
    u"""Class representing snake itself. It does not provide 'game' related utilities, like
    collision detection!"""

    def __init__(self, position: List[Vector2], player=True):
        u"""Position: list of tuples of int pairs indicating position of all fragments of body."""
        super(Snake, self).__init__(player)
        self.position = position
        self.length = len(self.position)

    def move(self, new_position: Vector2):
        u"""Snake does not move free, only incrementally."""
        raise NotImplementedError

    def move_incremental(self, direction: Vector2):
        u"""Move the snake for one field only."""
        self.position = [direction + self.position[0]] + self.position[:-1]

    def grow(self): # implement me!
        pass

    def __str__(self):
        return f"Snake of length {self.length} with head on position: {self.position[0]}"

    def __repr__(self):
        super().__repr__()


class AbstractController(metaclass=ABCMeta):
    u"""
        Abstract class for different types of player controls.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @abstractmethod
    def handle_control_on_player(cls, player: Actor, symbol: key):
        pass


class FourDirectionController(AbstractController):
    u"""
        Controller for movement in four direction: top, down, left, right.
        Actor is moved only when player provides input.
    """
    @classmethod
    def handle_control_on_player(cls, player: Actor, symbol: key):
        u"""Move player in four directions."""
        if symbol == player.input_map.move.top:
            player.move_incremental(Direction.top)
        elif symbol == player.input_map.move.down:
            player.move_incremental(Direction.down)
        elif symbol == player.input_map.move.left:
            player.move_incremental(Direction.left)
        elif symbol == player.input_map.move.right:
            player.move_incremental(Direction.right)


class SnakeController(AbstractController):
    u"""
        Snake-like controller. Player can only turn direction of movement to orthogonal of current direction.
        Snake moves forward if player has not provided any input.
    """
    @classmethod
    def handle_control_on_player(cls, player: Actor, symbol: key):
        u"""
            Move player to left or right in local space. Move forward if no actions was taken.
            Player can provide four different inputs for directions, although not all of them can be handled.
        """


class Game:

    class Drawings(Enum):
        snake = 0
        fruit = 1

    background_image = "background_anime.jpg"
    logger = logging.getLogger("Game")

    def __init__(self, w=640, h=480, speed=1, input_map=InputMap(),
                 snake: Snake = None, grid: Grid = Grid()):
        # Game objects
        self.snake = snake  # Snake should not known anything about grid
        self.grid = grid  # Grid should not known anything about snake
        self.speed = speed
        self.input_map = input_map

        # Software related objects
        h, w = self.grid.scale * self.grid.size
        self.window = pyglet.window.Window(height=h, width=w)

        # Additional info
        self.fps = pyglet.window.FPSDisplay(window=self.window)

        # I am not such a weeb, right? Also, Im not foot fetishist...
        with open(Game.background_image, 'rb') as image_bin:
            self.background_image = pyglet.image.load(filename=Game.background_image, file=image_bin)
        self.background_image = pyglet.sprite.Sprite(img=self.background_image)

    def wrap_position_on_grid(self):
        u"""Keep snake's position inside range(grid size)."""
        for position in self.snake.position:
            for i in (0, 1):
                if position[i] >= self.grid.size[i]:
                    position[i] = 0
                elif position[i] < 0:
                    position[i] = self.grid.size[i]

    def main(self):

        batch = pyglet.shapes.Batch()
        drawings = {Game.Drawings.snake: [],
                    Game.Drawings.fruit: []}  # cache drawings from local variables

        def draw_snake():
            drawings[Game.Drawings.snake].clear()  # clear drawings
            for position in self.snake.position:
                logger.debug(f"Position: {self.grid.grid_to_world(position)}")
                sh = shapes.Rectangle(*self.grid.grid_to_world(position), *self.grid.scale,
                                      color=(255, 0, 0), batch=batch)
                drawings[Game.Drawings.snake].append(sh)

        @self.window.event
        def on_key_press(symbol, modifiers):
            FourDirectionController().handle_control_on_player(self.snake, symbol)  # movement
            # Check if Snake's position is outside grid size! Snake and Grid have not idea about each other!
            self.wrap_position_on_grid()
            # begin of user interface handling and common utilities (pause, change speed, etc)
            if symbol == self.input_map.game.restart:
                pass
            elif symbol == self.input_map.game.start:
                pass
            elif symbol == self.input_map.game.speed_up:
                pass
            elif symbol == self.input_map.game.speed_down:
                pass

        @self.window.event
        def on_draw():
            self.window.clear()
            self.background_image.draw()
            self.fps.draw()
            draw_snake()
            batch.draw()

        pyglet.app.run()


if __name__ == '__main__':
    p = [Vector2(3, 3)]
    game = Game(snake=Snake(position=p))
    game.main()
