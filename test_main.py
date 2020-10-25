import unittest
from main import task_3


class TestNumbers(unittest.TestCase):
    def test_task_3_expected_res(self):
        t = (1, 1, 2, 3, 5, 8, 13)
        t2 = (1, 1)
        self.assertEqual(t, task_3(7))
        self.assertEqual(t2, task_3(2))

    def test_task_3_wrong_args(self):
        self.assertEqual(tuple(), task_3("chomik dżungarski"))
        self.assertEqual((1, 1), task_3(-10))

    def test_task_3_overflow_error(self):
        with self.assertRaises(OverflowError):
            task_3(23e412412412412)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
