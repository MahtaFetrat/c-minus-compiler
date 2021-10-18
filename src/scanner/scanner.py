"""This module contains the scanner of c-minus language."""

from file_handler import FileHandler


class Scanner:

    def __init__(self):
        self._file_handler = FileHandler("input.txt")

    @property
    def line_num(self):
        return self._file_handler.line_number

    def get_next_token(self):
        pass
