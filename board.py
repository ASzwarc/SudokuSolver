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

        def evaluate_point(solution_board, point, point_value):
            found_points = []
            for elem_no, elem in enumerate(solution_board[point.row]):
                if len(elem) > 1 and point_value in elem:
                    acc_val = solution_board[point.row][elem_no].replace(
                        point_value, '', 1)
                    if len(acc_val) == 1:
                        found_points.append(Point(point.row, elem_no))
                    solution_board[point.row][elem_no] = acc_val
            return found_points

        solution = []
        Point = namedtuple('Point', ['row', 'col'])
        found_points = []
        # row constraint
        for row in self._board:
            solution_row = []
            possible_values = "123456789"
            possible_values = possible_values.translate(
                {ord(str(i)): None for i in row})
            for elem in row:
                if elem != 0:
                    solution_row.append(str(elem))
                else:
                    solution_row.append(possible_values)
            solution.append(solution_row)
        # col constraint
        for col_iter in range(len(self._board[0])):
            col_constraint = [row[col_iter] for row in self._board
                              if row[col_iter] > 0]
            trans_dict = {ord(str(i)): None for i in col_constraint}
            for row_iter in range(len(self._board)):
                if len(solution[row_iter][col_iter]) > 1:
                    acc_vals = solution[row_iter][col_iter].translate(
                        trans_dict)
                    if len(acc_vals) == 1:
                        found_points.append(Point(row_iter, col_iter))
                    solution[row_iter][col_iter] = acc_vals
        print_it_nicely(solution)
        print(found_points)
        # box constraint
        for row_iter in range(0, 9, 3):
            for col_iter in range(0, 9, 3):
                flattened = [elem for row in solution[row_iter: row_iter + 3]
                             for elem in row[col_iter: col_iter + 3]]
                box_constraint_dict = {ord(i): None for i in
                                       [elem for elem in flattened
                                        if len(elem) == 1]}
                for elem_no, elem in enumerate(flattened):
                    if len(elem) > 1:
                        acc_vals = flattened[elem_no].translate(
                            box_constraint_dict)
                        solution[row_iter + (elem_no // 3)][col_iter +
                                                            (elem_no % 3)] =\
                            acc_vals
                        if len(acc_vals) == 1:
                            found_points.append(
                                Point(row_iter + (elem_no // 3),
                                      col_iter + (elem_no % 3)))
                print(found_points)
        print_it_nicely(solution)
        evaluate_point(solution, found_points[2],
                       solution[found_points[2].row][found_points[2].col])
        print_it_nicely(solution)


if __name__ == "__main__":
    board = Board(logging.DEBUG)
    board.add_row([0, 0, 0, 2, 6, 0, 7, 0, 1])
    board.add_row([6, 8, 0, 0, 7, 0, 0, 9, 0])
    board.add_row([1, 9, 0, 0, 0, 4, 5, 0, 0])
    board.add_row([8, 2, 0, 1, 0, 0, 0, 4, 0])
    board.add_row([0, 0, 4, 6, 0, 2, 9, 0, 0])
    board.add_row([0, 5, 0, 0, 0, 3, 0, 2, 8])
    board.add_row([0, 0, 9, 3, 0, 0, 0, 7, 4])
    board.add_row([0, 4, 0, 0, 5, 0, 0, 3, 6])
    board.add_row([7, 0, 3, 0, 1, 8, 0, 0, 0])
    board.pretty_print()
    board.solver()
