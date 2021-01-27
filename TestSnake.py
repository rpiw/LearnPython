import unittest
from Snake import *


class TestGrid(unittest.TestCase):
    def test_world_to_grid(self):
        samples = ((15, 14), (30, 28), (0, 0), (45, 0))
        expected_outputs = ((0, 0), (1, 1), (0, 0), (2, 0))
        grid = Grid(16, 16, 20, 20)
        for sample, output in zip(samples, expected_outputs):
            sample = Vector2(sample)
            output = Vector2(output)
            self.assertEqual(grid.world_to_grid(sample), output)

    def test_grid_to_world(self):
        grid = Grid(16, 16, 20, 20, "")
        samples = ((0, 0), (1, 1), (0, 1), (1, 0))
        excepted_outputs = ((0, 0), (16, 16), (0, 16), (16, 0))
        for sample, output in zip(samples, excepted_outputs):
            sample = Vector2(sample)
            output = Vector2(output)

            self.assertEqual(grid.grid_to_world(sample), output)


if __name__ == '__main__':
    unittest.main()
