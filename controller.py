from abc import ABCMeta, abstractmethod
from actor import Actor
from Vector import Direction
from pyglet.window import key


class AbstractController(metaclass=ABCMeta):
    u"""
        Abstract class for different types of player controls.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @classmethod
    @abstractmethod
    def handle_control_on_player(cls, player: Actor, symbol: key) -> Direction:
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
            requested_direction = Direction.top
        elif symbol == player.input_map.move.down:
            requested_direction = Direction.down
        elif symbol == player.input_map.move.left:
            requested_direction = Direction.left
        elif symbol == player.input_map.move.right:
            requested_direction = Direction.right
        else:
            requested_direction = Direction.zero

        return requested_direction


class SnakeController(AbstractController):
    u"""
        Snake-like controller. Player can only turn direction of movement to orthogonal of current direction.
        Snake moves forward if player has not provided any input.
    """
    direction = Direction.top

    @classmethod
    def handle_control_on_player(cls, player: Actor, symbol: key):
        u"""
            Move player to left or right in local space. Move forward if no actions was taken.
            Player can provide four different inputs for directions, although not all of them can be handled.
        """
        requested_direction = SnakeController.direction
        if symbol == player.input_map.move.top:
            requested_direction = Direction.top
        elif symbol == player.input_map.move.down:
            requested_direction = Direction.down
        elif symbol == player.input_map.move.left:
            requested_direction = Direction.left
        elif symbol == player.input_map.move.right:
            requested_direction = Direction.right

        if requested_direction.dot(SnakeController.direction) == 0:
            SnakeController.direction = requested_direction

        return SnakeController.direction
