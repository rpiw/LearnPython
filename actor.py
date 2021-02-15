from Vector import Vector2
from inputMap import InputMap
from abc import ABCMeta, abstractmethod
from typing import Union, List


class Actor(metaclass=ABCMeta):
    u"""ABC for all actors in a game."""

    @abstractmethod
    def __init__(self, position: Union[List[Vector2], Vector2], player=True, input_map=InputMap()):
        if not isinstance(position, (Vector2, List)):
            raise TypeError

        self.input_map = input_map
        self.player = player
        self.position = position

    def __repr__(self):
        return f"Class<Actor>: player: {self.player}"

    @abstractmethod
    def move(self, new_position: Vector2):
        u"""Move player to a new position."""

    @abstractmethod
    def move_incremental(self, direction: Vector2):
        u"""Move player incrementally from current position."""
