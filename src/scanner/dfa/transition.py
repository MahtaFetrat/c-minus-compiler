from typing import List

from src.scanner.dfa import State


class Transition(object):

    def __init__(self, symbols: List[str], dest_state: State):
        self._symbols = symbols
        self._dest_state = dest_state

    def __eq__(self, other):
        return (
                set(self._symbols) == set(other.symbols)
                and self._dest_state == other.dest_state
        )

    def is_valid(self, character) -> bool:
        return character in self._symbols
