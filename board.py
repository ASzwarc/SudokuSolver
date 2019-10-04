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
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging_level)
        streamHandler.setFormatter(
            logging.Formatter('%(name)s[%(levelname)s]: %(message)s'))
        logger = logging.getLogger(type(self).__name__)
        logger.setLevel(logging_level)
        logger.addHandler(streamHandler)
        return logger

    @property
    def board(self) -> List[List[int]]:
        """
        Items getter.

        Returns:
            List[List[int]] -- returns list of already filled elements, empty
            elemnts have value 0.
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
        for row in range(len(self._board)):
            self._logger.debug(" | ".join(
                [str(val) for val in self._board[row]]))
