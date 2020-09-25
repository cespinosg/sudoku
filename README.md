# sudoku
Sudoku reader and solver written in Python. This project was inspired by [Real Python's article "Python Practice Problems: Get Ready for Your Next Interview"](https://realpython.com/python-practice-problems/#python-practice-problem-5-sudoku-solver).

## Input

Input should be a single string where empty cells are marked with `"0"`. This is known as the [SDM format](http://www.sudocue.net/fileformats.php). For example, `"030100496005096210106000003980670031000000007000031000378415060400763080500928000"` maps to the sudoku below.

```
>>> sudoku = Sudoku("030100496005096210106000003980670031000000007000031000378415060400763080500928000")
>>> print(sudoku)
-------------------------
|   3   | 1     | 4 9 6 |
|     5 |   9 6 | 2 1   |
| 1   6 |       |     3 |
-------------------------
| 9 8   | 6 7   |   3 1 |
|       |       |     7 |
|       |   3 1 |       |
-------------------------
| 3 7 8 | 4 1 5 |   6   |
| 4     | 7 6 3 |   8   |
| 5     | 9 2 8 |       |
-------------------------
```
