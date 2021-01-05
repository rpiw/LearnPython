import unittest
from Snake import *
import numpy as np


class TestGrid(unittest.TestCase):
    def test_world_to_grid(self):
        samples = ((15, 14), (30, 28), (0, 0), (45, 0))
        expected_outputs = ((0, 0), (1, 1), (0, 0), (2, 0))
        grid = Grid(16, 16, 20, 20)
        for sample, output in zip(samples, expected_outputs):
            self.assertEqual(grid.world_to_grid(*sample), output)

    def test_grid_to_world(self):
        grid = Grid(16, 16, 20, 20, "")
        samples = ((0, 0), (1, 1), (0, 1), (1, 0))
        excepted_outputs = ((0, 0), (16, 16), (0, 16), (16, 0))
        for sample, output in zip(samples, excepted_outputs):
            self.assertEqual(grid.grid_to_world(*sample), output)


class TestSnake(unittest.TestCase):
    p = [(0, 0,), (0, 1), (0, 2)]

    def test_init(self):
        snake = Snake(TestSnake.p)
        self.assertEqual(len(TestSnake.p), snake.length)

    def test_move(self):
        snake = Snake(TestSnake.p)
        snake.move([1, 0])
        self.assertTrue(np.array_equal(snake.position[0], [1, 0]))
        self.assertTrue(np.array_equal(snake.position[-1], [0, 1]))

    def test_move_incremental(self):
        snake = Snake(TestSnake.p)
        snake.move_incremental(Direction.top)
        self.assertTrue(np.array_equal(snake.position[0], [-1, 0]))  # Move to legit position
        snake.move_incremental(Direction.down)


if __name__ == '__main__':
    unittest.main()
