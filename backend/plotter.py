import matplotlib.pyplot as plt


class Plotter:

    def __init__(self):
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_axes([0.05, 0.05, 0.9, 0.9])
        self.ax.axis("equal")
        self.ax.set_axis_off()
        self._major_grid()
        self._minor_grid()

    def _major_grid(self):
        for i in range(0, 28, 9):
            # vertical line
            self.ax.plot([i, i], [0, 27], lw=4, c="k")
            # horizontal line
            self.ax.plot([0, 27], [i, i], lw=4, c="k")

    def _minor_grid(self):
        for i in range(0, 28, 3):
            # vertical line
            self.ax.plot([i, i], [0, 27], lw=1, c="k")
            # horizontal line
            self.ax.plot([0, 27], [i, i], lw=1, c="k")

    def _write_number(self, i, j, num):
        self.ax.text(1.5+3*j, 25.5-0.1-3*i, num, ha="center", va="center", size=20)

    def _write_options(self, i, j, options):
        for o in options:
            self.ax.text(0.5+3*j+(o-1)%3, 26.5-0.05-3*i-int((o-1)/3), o, ha="center", va="center", size=7, color='grey')

    def plot(self, sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku.array[i, j] != 0:
                    self._write_number(i, j, sudoku.array[i, j])
                else:
                    self._write_options(i, j, sudoku.options[(i, j)])

    def show(self):
        plt.close(self.fig.number)
        self.fig.show()

    def save(self, path):
        self.fig.savefig(path, dpi=200, bbox_inches="tight")

