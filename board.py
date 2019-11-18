from typing import List
import logging
from collections import namedtuple


class Board():
    """
    Class for holding already filled sudoku board elements.
    """

    Point = namedtuple('Point', ['row', 'col', 'val'])

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

    def print_it_nicely(self, solution_board):
        print("\n")
        print("\n".join([" | ".join([elem.rjust(9, ' ') for elem in row])
                        for row in solution_board]))

    def _evaluate_col_constraint(self, solution_board, point):
        found_points = []
        for elem_no, elem in enumerate(solution_board[point.row]):
            if len(elem) > 1 and point.val in elem:
                acc_val = solution_board[point.row][elem_no].replace(
                    point.val, '', 1)
                if len(acc_val) == 1:
                    found_points.append(
                        self.Point(point.row, elem_no, acc_val))
                    self._logger.debug("Column eval: new point [%s, %s] = %s",
                                       point.row, elem_no, acc_val)
                solution_board[point.row][elem_no] = acc_val
        return found_points

    def _evaluate_row_constraint(self, solution_board, point):
        found_points = []
        for row_iter in range(len(solution_board)):
            elem = solution_board[row_iter][point.col]
            if len(elem) > 1 and point.val in elem:
                acc_val = elem.replace(point.val, '', 1)
                if len(acc_val) == 1:
                    found_points.append(self.Point(
                        row_iter, point.col, acc_val))
                    self._logger.debug("Row eval: new point [%s, %s] = %s",
                                       row_iter, point.col, acc_val)
                solution_board[row_iter][point.col] = acc_val
        return found_points

    def _evaluate_box_constraint(self, solution_board, point):
        found_points = []
        row_start = (point.row // 3) * 3
        col_start = (point.col // 3) * 3
        flattened = [elem for row in solution_board[row_start:row_start+3]
                     for elem in row[col_start:col_start+3]]
        for i, elem in enumerate(flattened):
            if len(elem) > 1 and point.val in elem:
                acc_val = elem.replace(point.val, '', 1)
                row = row_start + (i // 3)
                col = col_start + (i % 3)
                if len(acc_val) == 1:
                    found_points.append(self.Point(row, col, acc_val))
                    self._logger.debug("Box eval: new point [%s, %s] = %s",
                                       row, col, acc_val)
                solution_board[row][col] = acc_val
        return found_points

    def _evaluate_point(self, solution_board, point):
        found_points = []
        found_points.extend(self._evaluate_col_constraint(
            solution_board, point))
        found_points.extend(self._evaluate_row_constraint(
            solution_board, point))
        found_points.extend(self._evaluate_box_constraint(
            solution_board, point))
        return found_points

    def _init_solution_board(self):
        initial_value = "123456789"
        solution = [[initial_value for col in range(len(self._board[0]))]
                    for row in range(len(self._board))]
        found_points = []
        for row_iter, row in enumerate(self._board):
            for col_iter, elem in enumerate(row):
                if elem != 0:
                    solution[row_iter][col_iter] = str(elem)
                    found_points.append(self.Point(
                        row_iter, col_iter, str(elem)))
        return solution, found_points

    def _find_point_to_process(self, solution_board):
        shortest_point_len = 9
        for row_no in range(len(solution_board)):
            for col_no in range(len(solution_board[0])):
                point = solution_board[row_no][col_no]
                if (len(point) < shortest_point_len) and len(point) > 1:
                    shortest_point_len = len(point)
                    evaluation_point = self.Point(row_no, col_no, point)
        return evaluation_point

    def solver(self):
        points_to_find = 81
        solution, found_points = self._init_solution_board()
        points_to_find -= len(found_points)
        self.print_it_nicely(solution)
        self._logger.debug("Found points evaluation")
        for point in found_points:
            self._logger.debug("Evaluating Point(%s, %s)=%s",
                               point.row, point.col, point.val)
            new_points = self._evaluate_point(solution, point)
            found_points.extend(new_points)
            points_to_find -= len(new_points)
        if points_to_find == 0:
            self._logger.info("Found solution:")
            self.print_it_nicely(solution)
            return
        else:
            self._logger.debug("No of points to find: %s", points_to_find)
            next_point = self._find_point_to_process(solution)
            self._logger.debug("Next point to process: (%s, %s)=%s",
                               next_point.row, next_point.col, next_point.val)
            # Algorithm:
            # 1. search for the point with least amount of possible numbers
            # 2. make an assumption and remember it
            # 3. try to solve board


if __name__ == "__main__":
    board = Board(logging.DEBUG)
    # Board taken from:
    # https://dingo.sbs.arizona.edu/~sandiway/sudoku/examples.html
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
