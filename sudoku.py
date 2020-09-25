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
        self.zero_cells = [(i, j) for i in range(9) for j in range(9) if self.array[i, j] == 0]

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

    def iterate(self):
        """
        Looks for the options at all empty cells.
        If only one option is identified, it is stored as the solution.
        """
        new_zeros = []
        n_sols = 0
        for ij in self.zero_cells: # loops only over empty cells
                options = self.get_cell_options(*ij)
                if len(options) == 1:
                    self.array[ij] = options[0]
                    n_sols += 1
                else:
                    new_zeros.append(ij)
                # TODO: if the option is the only available in the row, column or square, it should be used.
        self.zero_cells = new_zeros # update the empty cells list
        self.iterations += 1
        self.sol_evol.append(n_sols)

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
            n_zeros = len(self.zero_cells)
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
    ln = "".join(medium)
    print(f"\ninput: \"{ln}\"\n")
    sudoku = Sudoku(ln)
    print(f"sudoku:\n{sudoku}\n")
    #print(f"sudoku.array:\n{sudoku.array}\n")
    print(f"Options for cell (2, 3): {sudoku.get_cell_options(2, 3)}\n")
    sudoku.solve()
