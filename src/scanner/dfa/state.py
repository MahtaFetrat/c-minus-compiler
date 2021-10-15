from enum import Enum
from typing import List

from src.scanner.dfa import Transition, TransferException


class StateType(Enum):
    START = 'start'
    END = 'end'
    MIDDLE = 'middle'


class State(object):

    def __init__(self, transitions: List[Transition], state_type: StateType):
        self._transitions = transitions
        self.type = state_type

    def transfer(self, character: str):
        try:
            return list(filter(lambda x: x.is_valid(character), self._transitions))[0]
        except IndexError:
            raise TransferException

    def is_final(self) -> bool:
        return self.type == StateType.END
