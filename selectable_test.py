import unittest
from selectable import SelectableList


class SelectableListTest(unittest.TestCase):

    def test_init(self):
        a = SelectableList([1, 2, 3, 4, 5, 6])

        self.assertTrue(len(a) == 6)
        self.assertListEqual(a, [1, 2, 3, 4, 5, 6])

        self.assertEqual(0, a.index)

        with self.assertRaises(TypeError):
            SelectableList((1, 2, 3))

    def test_next(self):
        a = SelectableList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], chain=True)
        for i in range(0, 2 * len(a)):
            i = i % len(a)
            self.assertEqual(i, a.selected_index)
            next(a)

        b = SelectableList([1, 2, 3], chain=False)

        with self.assertRaises(StopIteration):
            for i in range(0, 20):
                next(b)
        self.assertEqual(b.selected_index, 0)
        b.restart_iterator()
        for i in b._iterator:
            print(i, b.selected_index)

        # for i in range(len(b)):
        #     self.assertEqual(i, b.selected_index)


if __name__ == '__main__':
    unittest.main()
