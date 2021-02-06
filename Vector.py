from collections import Sequence
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

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"Vector2 x={self.x}, y={self.y}"

    def __repr__(self):
        return f"{self.x, self.y}"

    def __iter__(self):
        return iter((self.x, self.y))