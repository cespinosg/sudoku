import itertools

import matplotlib.pyplot as plt
import numpy as np


class Sudoku:
    '''
    Stores and solves a sudoku.
    '''

    def __init__(self, line):
        self.sdm = line
        self._build()
        self._set_groups()

    def _build(self):
        '''
        Stores the sudoku into an array.
        '''
        numbers = [int(l) for l in self.sdm]
        array = [numbers[9*i:9*(i+1)] for i in range(9)]
        self.array = np.array(array)
        indices = [i for i in range(9)]
        self.cells = np.array([[Cell(self.array[i, j], i, j) for j in indices] for i in indices])

    def _set_groups(self):
        '''
        Sets the groups of cells useful for solving the sudoku.
        '''
        self.rows = [Group(self.cells[i, :]) for i in range(9)]
        self.cols = [Group(self.cells[:, i]) for i in range(9)]
        indices = itertools.product([0, 1, 2], repeat=2)
        self.squares = [0 for i in range(9)]
        for k in range(9):
            (i, j) = next(indices)
            cells = self.cells[3*i:3*(i+1), 3*j:3*(j+1)].flatten()
            self.squares[k] = Group(cells)

    def __repr__(self):
        '''
        Creates the sudoku string representation.
        '''
        lns = [[str(cell.value) for cell in row] for row in self.cells]
        lns = ['| '+' | '.join([' '.join(ln[3*i:3*(i+1)]) for i in range(3)])+' |' for ln in lns]
        hrule = ['-'*len(lns[0])]
        lns = [hrule+lns[3*i:3*(i+1)] for i in range(3)]
        lns = [lni for ln in lns for lni in ln]
        lns = lns+hrule
        return '\n'.join(lns).replace('0', ' ')

    def update_options(self):
        '''
        Updates the cell options.
        '''
        for i in range(9):
            self.rows[i].update_cell_options()
            self.cols[i].update_cell_options()
            self.squares[i].update_cell_options()


class Cell:
    '''
    Represents a cell in the sudoku.
    '''

    def __init__(self, value, i, j):
        self.value = value
        self.i = i
        self.j = j
        self.options = [i for i in range(1, 10)] if value == 0 else []

    def remove_options(self, values):
        '''
        Removes the given values from the list of options.
        '''
        self.options = [o for o in self.options if o not in values]
        if len(self.options) == 1:
            self.value = self.options[0]
            self.options = []
            print(f'Cell[{self.i+1}, {self.j+1}] = {self.value}')


class Group:
    '''
    Represents a group of cells.
    '''

    def __init__(self, cells):
        self.cells = cells
        self.set_values()

    def set_values(self):
        '''
        Sets the values of the group.
        '''
        self.values = sorted([c.value for c in self.cells if c.value != 0])

    def update_cell_options(self):
        '''
        Updates the cells options based on the group values.
        '''
        self.set_values()
        [c.remove_options(self.values) for c in self.cells]
        self.set_values()


if __name__ == '__main__':
    easy = [
            '030100496',
            '005096210',
            '106000003',
            '980670031',
            '000000007',
            '000031000',
            '378415060',
            '400763080',
            '500928000',
           ]
    medium = [
              '006000700',
              '040000510',
              '801000069',
              '030000006',
              '500612000',
              '700000102',
              '407093005',
              '003024000',
              '000007423',
           ]
    hard = [
            '000000687',
            '000000900',
            '000608050',
            '000000060',
            '085120009',
            '210046000',
            '473000001',
            '800090000',
            '020007000',
           ]
    expert = [
              '040005870',
              '000000100',
              '090000002',
              '000070400',
              '051300007',
              '003006000',
              '005002090',
              '000508600',
              '000064000',
             ]
    # source for sudokus: https://sudoku.com/es/normal/
    ln = ''.join(easy)
    print(f'\ninput: \'{ln}\'\n')
    sudoku = Sudoku(ln)
    print(f'sudoku:\n{sudoku}\n')

