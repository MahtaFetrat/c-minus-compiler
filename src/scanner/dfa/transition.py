from typing import List

from src.scanner.dfa import State


class Transition(object):

    def __init__(self, symbols: List[str], dest: State):
        self._symbols = symbols
        self._dest = dest

    def is_valid(self, character) -> bool:
        return character in self._symbols
