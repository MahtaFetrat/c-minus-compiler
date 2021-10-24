from typing import List

from ..utils import TransitionType


class Transition:

    def __init__(self, symbols: List[str], dest_state,
                 transition_type: TransitionType = TransitionType.INCLUDE):
        self.dest_state = dest_state
        self._symbols = symbols or []
        self.type = transition_type or TransitionType.INCLUDE

    def __eq__(self, other):
        return bool(
            set(self._symbols) == set(other.symbols)
            and self.dest_state == other.dest_state
            and self.type == other.type
        )

    def __str__(self):
        return ' --%s--> %s' % (self._symbols, self.dest_state.state_id)

    def is_include(self) -> bool:
        return self.type == TransitionType.INCLUDE

    def is_valid(self, character) -> bool:
        return bool((contains := character in self._symbols and self.is_include())
                    or not (contains or self.is_include()))

    @property
    def symbols(self):
        return self._symbols.copy()
