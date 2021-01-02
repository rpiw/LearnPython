# Sudoku solver
import numpy as np


class Sudoku:

    def __init__(self, sudoku, square_size=3, grid_size=9):
        self.sudoku = np.array(sudoku, dtype=int)
        self.grid_size = grid_size
        self.square_size = square_size
        self.solved = 0 not in self.sudoku

    def __repr__(self):
        return repr(self.sudoku)

    def check(self, x, y, number):
        # Determine columns and rows
        for i in range(self.grid_size):
            if self.sudoku[x, i] == number:
                return False
            if self.sudoku[i, y] == number:
                return False
        # Determine the square
        square_x = x // self.square_size * self.square_size
        square_y = y // self.square_size * self.square_size
        for i in range(0, 3):
            for j in range(0, 3):
                _x, _y = square_x + i, square_y + j
                if self.sudoku[_x, _y] == number:
                    return False
        return True

    def solve(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.sudoku[x, y] == 0:
                    for n in range(1, self.grid_size + 1):
                        if self.check(x, y, n):
                            self.sudoku[x, y] = n
                            self.solve()
                            self.sudoku[x, y] = 0
                    return
        self.solved = True

    @staticmethod
    def read_from_file(file_name, grid_size=9):
        with open(file_name, 'r') as fi:
            lines = fi.readlines()
        sudokus = []
        sudoku = []
        for line in lines:
            line = line.replace('\n', '')
            if line.isdigit():
                sudoku.append([int(x) for x in line])
            if len(sudoku) == grid_size:
                sudokus.append(sudoku)
                sudoku = []
        return list(Sudoku(sudoku) for sudoku in sudokus)
