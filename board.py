from typing import List
import logging


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
        solution = []
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
        self._logger.debug(solution)
        # col constraint
        for col_iter in range(len(self._board[0])):
            col_constraint = [row[col_iter] for row in self._board
                              if row[col_iter] > 0]
            trans_dict = {ord(str(i)): None for i in col_constraint}
            for row_iter in range(len(self._board)):
                solution[row_iter][col_iter] =\
                    solution[row_iter][col_iter].translate(trans_dict)
        self._logger.debug(solution)


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
