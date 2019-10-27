from typing import List
import logging
from collections import namedtuple


class Board():
    """
    Class for holding already filled sudoku board elements.
    """
    def __init__(self, logging_level) -> None:
        """
        Empty initialises Board.
        """
        self._board = []
        self._logger = self._set_logger(logging_level)

    def _set_logger(self, logging_level):
        logging.basicConfig(format='%(name)s[%(levelname)s]: %(message)s')
        logger = logging.getLogger(type(self).__name__)
        logger.setLevel(logging_level)
        return logger

    @property
    def board(self) -> List[List[int]]:
        """
        Items getter.

        Returns:
            List[List[int]] -- returns list of already filled elements, empty
            elements have value 0.
        """
        return self._board

    def add_row(self, row: List[int]):
        """
        Adds next row to the board

        Arguments:
            row {List[int]} -- row to be added
        """
        if len(row) < 9:
            raise IndexError(f"{type(self).__name__}.add_row:" +
                             f"row should have 9 elements not {len(row)}")
        if len(self._board) < 9:
            self._board.append(row)
        else:
            raise IndexError(f"{type(self).__name__}.add_row:" +
                             "board can only have 9!")

    def pretty_print(self):
        """
        Prints whole board nicely.
        """
        for row in range(len(self._board)):
            self._logger.debug("|".join(
                [str(val) if val > 0 else " " for val in self._board[row]]))
            if row < 8:
                self._logger.debug("-" * 18)

    def solver(self):
        def print_it_nicely(solution_board):
            print("\n")
            print("\n".join([" | ".join([elem.rjust(9, ' ') for elem in row])
                            for row in solution_board]))

        def evaluate_point(solution_board, point):
            found_points = []
            for elem_no, elem in enumerate(solution_board[point.row]):
                if len(elem) > 1 and point.val in elem:
                    acc_val = solution_board[point.row][elem_no].replace(
                        point.val, '', 1)
                    if len(acc_val) == 1:
                        found_points.append(Point(point.row, elem_no, acc_val))
                        self._logger.debug("Row eval: new point [%s, %s] = %s",
                                           point.row, elem_no, acc_val)
                    solution_board[point.row][elem_no] = acc_val
            for row_iter in range(len(solution_board)):
                elem = solution_board[row_iter][point.col]
                if len(elem) > 1 and point.val in elem:
                    acc_val = elem.replace(point.val, '', 1)
                    if len(acc_val) == 1:
                        found_points.append(Point(
                            row_iter, point.col, acc_val))
                        self._logger.debug(
                            "Column eval: new point [%s, %s] = %s",
                            row_iter, point.col, acc_val)
                    solution_board[row_iter][point.col] = acc_val
            for row_iter in range(0, len(solution_board), 3):
                for col_iter in range(0, len(solution_board[0]), 3):
                    flattened = [elem for row in
                                 solution_board[row_iter:row_iter+3]
                                 for elem in row[col_iter:col_iter+3]]
                    for elem in flattened:
                        if len(elem) > 1 and point.val in elem:
                            acc_val = elem.replace(point.val, '', 1)
                            row = row_iter + (elem_no // 3)
                            col = col_iter + (elem_no % 3)
                            if len(acc_val) == 1:
                                found_points.append(Point(row, col, acc_val))
                                self._logger.debug(
                                    "Box eval: new point [%s, %s] = %s", row,
                                    col, acc_val)
            return found_points

        initial_value = "123456789"
        solution = [[initial_value for col in range(len(self._board[0]))]
                    for row in range(len(self._board))]
        Point = namedtuple('Point', ['row', 'col', 'val'])
        found_points = []
        for row_iter, row in enumerate(self._board):
            for col_iter, elem in enumerate(row):
                if elem != 0:
                    solution[row_iter][col_iter] = str(elem)
                    found_points.append(Point(row_iter, col_iter, str(elem)))

        print_it_nicely(solution)
        self._logger.debug("Found points evaluation")
        for point in found_points:
            self._logger.debug("Evaluating Point(%s, %s)=%s",
                               point.row, point.col, point.val)
            found_points.extend(evaluate_point(solution, point))
        print_it_nicely(solution)


if __name__ == "__main__":
    board = Board(logging.DEBUG)
    board.add_row([0, 2, 0, 6, 0, 8, 0, 0, 0])
    board.add_row([5, 8, 0, 0, 0, 9, 7, 0, 0])
    board.add_row([0, 0, 0, 0, 4, 0, 0, 0, 0])
    board.add_row([3, 7, 0, 0, 0, 0, 5, 0, 0])
    board.add_row([6, 0, 0, 0, 0, 0, 0, 0, 4])
    board.add_row([0, 0, 8, 0, 0, 0, 0, 1, 3])
    board.add_row([0, 0, 0, 0, 2, 0, 0, 0, 0])
    board.add_row([0, 0, 9, 8, 0, 0, 0, 3, 6])
    board.add_row([0, 0, 0, 3, 0, 6, 0, 9, 0])
    board.pretty_print()
    board.solver()
