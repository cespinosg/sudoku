import numpy as np


class Sudoku:

    def __init__(self, line):
        self.sdm = line
        self.build(line)
        self.iterations = 0 # number of iterations performed trying to solve the sudoku
        self.sol_evol = [] # number of solutions found at each iteration

    def build(self, line):
        """
        Stores the sudoku into an array.
        """
        numbers = [int(l) for l in line]
        array = [numbers[9*i:9*(i+1)] for i in range(9)]
        self.array = np.array(array)
        # find empty cells (useful for solving the sudoku)
        zero_cells = [(i, j) for i in range(9) for j in range(9) if self.array[i, j] == 0]
        self.options = {ij: [] for ij in zero_cells}

    def __repr__(self):
        """
        Creates the sudoku string representation.
        """
        lns = [[str(aij) for aij in ai] for ai in self.array]
        lns = ["| "+" | ".join([" ".join(ln[3*i:3*(i+1)]) for i in range(3)])+" |" for ln in lns]
        hrule = ["-"*len(lns[0])]
        lns = [hrule+lns[3*i:3*(i+1)] for i in range(3)]
        lns = [lni for ln in lns for lni in ln]
        lns = lns+hrule
        return "\n".join(lns).replace("0", " ")

    def get_cell_options(self, i, j):
        """
        Returns a list of options at the given cell.
        """
        if self.array[i, j] == 0:
            options = [i for i in range(1, 10)]
            row = [r for r in self.array[i, :] if r != 0]
            col = [c for c in self.array[:, j] if c != 0]
            si = int(i/3)*3
            sj = int(j/3)*3
            square = [aij for ai in self.array[si:si+3] for aij in ai[sj:sj+3] if aij != 0]
            not_available = set(row+col+square)
            options = [o for o in options if o not in not_available]
            # print(f"row={row}")
            # print(f"col={col}")
            # print(f"square={square}")
            # print(f"not_available={not_available}")
        else:
            options = []
        return options

    def limit_cell_options(self, i, j):
        """
        Limits the cell options in case an option is the only one in
        its row, column or square.
        """
        # get index of empty cells in row, column and square (skip given cell)
        row = [ij for ij in self.options if ij[0] == i and ij[1] != j]
        col = [ij for ij in self.options if ij[1] == j and ij[0] != i]
        si = int(i/3)*3
        sj = int(j/3)*3
        square = [ij for ij in self.options if si <= ij[0] and ij[0] < si+3]
        square = [ij for ij in square if sj <= ij[1] and ij[1] < sj+3]
        square = [ij for ij in square if ij[0] != i or ij[1] != j]
        # get options for row, column and square
        row_opts = [o for ij in row for o in self.options[ij]]
        col_opts = [o for ij in col for o in self.options[ij]]
        sq_opts = [o for ij in square for o in self.options[ij]]
        # find cell options not present in row, column and square
        not_in_row = [o for o in self.options[i, j] if o not in row_opts]
        not_in_col = [o for o in self.options[i, j] if o not in col_opts]
        not_in_sq = [o for o in self.options[i, j] if o not in sq_opts]
        if len(not_in_row) == 1:
            self.options[i, j] = not_in_row
        elif len(not_in_col) == 1:
            self.options[i, j] = not_in_col
        elif len(not_in_sq) == 1:
            self.options[i, j] = not_in_sq

    def iterate(self):
        """
        Looks for the options at all empty cells.
        If only one option is identified, it is stored as the solution.
        """
        new_zeros = []
        n_sols = 0
        self.options = {ij: self.get_cell_options(*ij) for ij in self.options}
        [self.limit_cell_options(*ij) for ij in self.options]
        for ij in self.options: # loops only over empty cells
                if len(self.options[ij]) == 1:
                    self.array[ij] = self.options[ij][0]
                    n_sols += 1
                else:
                    new_zeros.append(ij)
        self.options = {ij: self.options[ij] for ij in new_zeros} # update the empty cells list
        self.iterations += 1
        self.sol_evol.append(n_sols)

    def print_options(self):
        """
        Prints a list of the options for each empty cell.
        """
        print("\nOptions for the empty cells:\n")
        print("\n".join(f"{o}: {self.options[o]}" for o in self.options))

    def solve(self):
        """
        Tries to solve the sudoku.
        """
        n_zeros_old = 81
        n_zeros = n_zeros_old-1
        # iterate while the solution progresses
        while n_zeros != n_zeros_old and n_zeros > 0:
            self.iterate()
            n_zeros_old = n_zeros
            n_zeros = len(self.options)
        if n_zeros == 0:
            print(f"The sudoku was solved with {self.iterations} iterations!")
        else:
            print(f"No solution was found for the sudoku. {self.iterations} iterations were performed.")


if __name__ == "__main__":
    easy = [
            "030100496",
            "005096210",
            "106000003",
            "980670031",
            "000000007",
            "000031000",
            "378415060",
            "400763080",
            "500928000",
           ]
    medium = [
              "006000700",
              "040000510",
              "801000069",
              "030000006",
              "500612000",
              "700000102",
              "407093005",
              "003024000",
              "000007423",
           ]
    hard = [
            "000000687",
            "000000900",
            "000608050",
            "000000060",
            "085120009",
            "210046000",
            "473000001",
            "800090000",
            "020007000",
           ]
    expert = [
              "040005870",
              "000000100",
              "090000002",
              "000070400",
              "051300007",
              "003006000",
              "005002090",
              "000508600",
              "000064000",
             ]
    # source for sudokus: https://sudoku.com/es/normal/
    ln = "".join(expert)
    print(f"\ninput: \"{ln}\"\n")
    sudoku = Sudoku(ln)
    print(f"sudoku:\n{sudoku}\n")
    #print(f"sudoku.array:\n{sudoku.array}\n")
    print(f"Options for cell (2, 3): {sudoku.get_cell_options(2, 3)}\n")
    sudoku.solve()
