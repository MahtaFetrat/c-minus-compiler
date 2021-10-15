from enum import Enum
from typing import List

from scanner.scanner import Transition


class StateType(Enum):
    START = 'start'
    END = 'end'
    MIDDLE = 'middle'


class State(object):

    def __init__(self, transitions: List[Transition], state_type: StateType):  # TODO
        self._transitions = transitions
        self.type = state_type

    def transfer(self, character: str):  # -> TODO
        # return state
        pass

    def is_final(self):
        return self.type == StateType.END
