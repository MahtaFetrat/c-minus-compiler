from typing import List

from src.scanner.dfa import Transition, TransferException
from src.scanner.utils.enums import StateType


class State(object):

    def __init__(self, state_id: str, state_type: StateType, transitions: List[Transition] = None):
        self.state_id = state_id
        self._transitions = transitions or []
        self._type = state_type

    def __eq__(self, other):
        return self.state_id == other.state_id

    def transfer(self, character: str):
        try:
            return list(filter(lambda x: x.is_valid(character), self._transitions))[0]
        except IndexError:
            raise TransferException

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    def is_final(self) -> bool:
        return self._type == StateType.END
