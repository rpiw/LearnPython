from pyglet.window import key


class InputMap:
    u"""Template input map."""

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
