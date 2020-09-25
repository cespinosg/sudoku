import numpy as np


class Sudoku:

    def __init__(self, line):
        self.build(line)

    def build(self, line):
        """
        Stores the sudoku into an array.
        """
        numbers = [int(l) for l in line]
        array = [numbers[9*i:9*(i+1)] for i in range(9)]
        self.array = np.array(array)

    def __str__(self):
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

    def get_options(self, i, j):
        """
        Returns a list of options at the given cell.
        """
        options = [i for i in range(1, 9)]
        row = self.array[i, :]
        col = self.array[:, j]
        si = int(i/3)
        sj = int(i/3)
        square = [aij for ai in self.array[si:si+3] for aij in ai[sj:sj+3]]
        options = [o for o in options if o not in row]
        options = [o for o in options if o not in col]
        options = [o for o in options if o not in square]
        return options


if __name__ == "__main__":
    ln = ["030100496",
          "005096210",
          "106000003",
          "980670031",
          "000000007",
          "000031000",
          "378415060",
          "400763080",
          "500928000",
         ]
    ln = "".join(ln)
    sudoku = Sudoku(ln)
    print(f"sudoku.array:\n{sudoku.array}")
