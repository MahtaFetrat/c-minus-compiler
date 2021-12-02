from abc import ABC
from copy import deepcopy
from typing import List


class Edge(ABC):

    def __init__(self, symbols: List, dest):
        self.dest = dest
        self._symbols = symbols or []

    def __eq__(self, other):
        return bool(
            set(self._symbols) == set(other.symbols)
            and self.dest == other.dest
        )

    def __str__(self):
        return ' --%s--> %s' % (self._symbols, self.dest.identifier)

    @property
    def symbols(self):
        return deepcopy(self._symbols)

    def is_valid(self, character: str):
        raise NotImplementedError
