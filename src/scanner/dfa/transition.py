from typing import List


class Transition(object):

    def __init__(self, symbols: List[str], dest_state):
        self._symbols = symbols
        self.dest_state = dest_state

    def __eq__(self, other):
        return bool(
                set(self._symbols) == set(other.symbols)
                and self.dest_state == other.dest_state
        )

    def is_valid(self, character) -> bool:
        return character in self._symbols

    @property
    def symbols(self):
        return self._symbols.copy()
