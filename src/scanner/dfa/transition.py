from typing import List

from src.base import Edge
from src.scanner.utils import TransitionType


class Transition(Edge):

    def __init__(self, symbols: List[str], dest,
                 transition_type: TransitionType = TransitionType.INCLUDE):

        super().__init__(symbols, dest)
        self.type = transition_type or TransitionType.INCLUDE

    def __eq__(self, other):
        return bool(
            super().__eq__(other)
            and self.type == other.type
        )

    def is_include(self) -> bool:
        return self.type == TransitionType.INCLUDE

    def is_valid(self, character) -> bool:
        return bool((contains := character in self._symbols and self.is_include())
                    or not (contains or self.is_include()))
