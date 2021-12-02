from typing import List

from src.base import Node
from src.parser.diagram.transition import Transition


class State(Node):
    def __init__(self,
                 identifier: int,
                 final: bool = False,
                 error: bool = False,
                 transitions: List[Transition] = None):
        self.final = final
        self.error = error
        super(State, self).__init__(identifier, transitions)

    def transfer(self, character: str):
        try:
            state = list(filter(lambda x: x.is_valid(character), self._edges))[0].dest_state
            return state
        except IndexError:
            return InvalidState(self.identifier)

    def is_final(self) -> bool:
        return self.final

    def is_error(self) -> bool:
        return self.error

    @property
    def transition(self):
        return self._edges[0]


class InvalidState(State):

    def __init__(self, identifier):
        super().__init__(identifier)

    def transfer(self, character: str):
        return self
