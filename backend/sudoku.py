import itertools

import matplotlib.pyplot as plt
import numpy as np

import plotter as plot


class Sudoku:
    '''
    Stores and solves a sudoku.
    '''

    def __init__(self, line):
        self.sdm = line
        self._build()
        self._set_groups()
        self._set_options()

    def _build(self):
        '''
        Stores the sudoku into an array.
        '''
        numbers = [int(l) for l in self.sdm]
        array = [numbers[9*i:9*(i+1)] for i in range(9)]
        self.array = np.array(array)
        self.cells = np.array([[Cell(ri) for ri in r] for r in self.array])
        self.n_solved_cells = sum([ni > 0 for ni in numbers])

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

    def _set_options(self):
        '''
        Sets the cell options.
        '''
        for i in range(9):
            self.rows[i].update_options()
            self.cols[i].update_options()
            self.squares[i].update_options()
        self._set_n_options()

    def _set_n_options(self):
        '''
        Sets the number of options.
        '''
        self.n_options = sum([len(c.options) for c in self.cells.flatten()])

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

    def is_solved(self):
        '''
        Checks if the sudoku is solved.
        '''
        rows = all([r.is_solved() for r in self.rows])
        cols = all([c.is_solved() for c in self.cols])
        squares = all([s.is_solved() for s in self.squares])
        return all([rows, cols, squares])

    def solve(self):
        '''
        Solves the sudoku.
        '''
        n_solved_cells_old = 0
        n_options_old = self.n_options
        self.iterations = 0
        while any([n_solved_cells_old < self.n_solved_cells,
            self.n_options < n_options_old]):
            print(f'\nIteration {self.iterations}')
            n_solved_cells_old = self.n_solved_cells
            n_options_old = self.n_options
            self.iterate()
            self.iterations += 1

    def iterate(self):
        '''
        Does one iteration to solve the sudoku.
        '''
        print('Before passing')
        print(f'  Solved cells: {self.n_solved_cells}')
        print(f'  Options: {self.n_options}')
        for i in range(9):
            for j in range(9):
                self._trim_groups_options(i, j)
                if len(self.cells[i, j].options) == 1:
                    self._solve_cell(i, j, self.cells[i, j].options[0])
                self._check_unique_option(i, j)
        self._set_n_options()
        print('After passing')
        print(f'  Solved cells: {self.n_solved_cells}')
        print(f'  Options: {self.n_options}')

    def _trim_groups_options(self, i, j):
        '''
        Trims the groups options.
        '''
        k = int(i/3)*3+int(j/3)
        self.rows[i].trim_options()
        self.cols[j].trim_options()
        self.squares[k].trim_options()

    def _check_unique_option(self, i, j):
        '''
        Checks if the given cell has a unique option among its groups.
        '''
        k = int(i/3)*3+int(j/3)
        only_option_in_row = self.rows[i].check_cell(self.cells[i, j])
        only_option_in_col = self.cols[j].check_cell(self.cells[i, j])
        only_option_in_s = self.squares[k].check_cell(self.cells[i, j])
        if only_option_in_row is not None:
            self._solve_cell(i, j, only_option_in_row)
        elif only_option_in_col is not None:
            self._solve_cell(i, j, only_option_in_col)
        elif only_option_in_s is not None:
            self._solve_cell(i, j, only_option_in_s)

    def _solve_cell(self, i, j, value):
        '''
        Sets the given value to the given cell.
        '''
        self.cells[i, j].solve(value)
        self.rows[i].update()
        self.cols[j].update()
        k = int(i/3)*3+int(j/3)
        self.squares[k].update()
        self.n_solved_cells += 1


class Cell:
    '''
    Represents a cell in the sudoku.
    '''

    def __init__(self, value):
        self.value = value
        self.options = [i for i in range(1, 10)] if value == 0 else []

    def remove_options(self, values):
        '''
        Removes the given values from the list of options.
        '''
        self.options = [o for o in self.options if o not in values]

    def solve(self, value):
        '''
        Sets the cell value.
        '''
        self.value = value
        self.options = []


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
        self.unsolved_ids = [i for i in range(9) if self.cells[i].value == 0]

    def update_options(self):
        '''
        Updates the cells options based on the group values.
        '''
        [c.remove_options(self.values) for c in self.cells]

    def update(self):
        '''
        Updates the group values and options.
        '''
        self.set_values()
        self.update_options()

    def is_solved(self):
        '''
        Checks if the group is solved.
        '''
        return len(set(self.values)) == 9

    def check_cell(self, cell):
        '''
        Looks if the given cell has missing values that are only feasible there.
        '''
        other_cells = [c for c in self.cells if c != cell]
        other_options = [c.options for c in other_cells]
        other_options = sorted(set([oi for o in other_options for oi in o]))
        value = [o for o in cell.options if o not in other_options]
        if len(value) == 1:
            return value[0]
        else:
            return None

    def trim_options(self):
        '''
        Checks the options in the group and removes them if a subgroup has a
        closed set of options.
        
        For example, if two cells only can be 1 or 2, these options
        can be removed from the rest of cells.
        '''
        self.find_closed_subgroups(2)
        self.find_closed_subgroups(3)

    def find_closed_subgroups(self, n):
        '''
        Finds subgroups with a closed set of options with the given size.
        '''
        for subgroup_indices in itertools.combinations(self.unsolved_ids, n):
            options = self.get_subgroup_options(subgroup_indices)
            if len(options) == len(subgroup_indices):
                for k in self.unsolved_ids:
                    if k not in subgroup_indices:
                        self.cells[k].remove_options(options)

    def get_subgroup_options(self, indices):
        '''
        Returns the options of the given subgroup.
        '''
        return sorted(set([o for i in indices for o in self.cells[i].options]))


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
    ln = ''.join(expert)
    print(f'\ninput: \'{ln}\'\n')
    sudoku = Sudoku(ln)
    print(f'sudoku:\n{sudoku}\n')
    plotter = plot.Plotter(sudoku)
    plotter.plot()

