from typing import Tuple

from src.scanner.dfa.state import State
from src.scanner.utils import StateActionType, TransferException


class DFA(object):

    def __init__(self, start_state):
        self._start_state = start_state

    def iterate(self, string) -> State:
        state = self._start_state
        for character in string:
            state = state.transfer(character)
        return state

    def accepts(self, string) -> Tuple[bool, StateActionType]:
        try:
            state = self.iterate(string)
            if state.role_back and state.is_final():
                return True, StateActionType.ROLE_BACK
            if state.is_final():
                return True, StateActionType.REGULAR
            else:
                return False, StateActionType.UNFINISHED_EXP
        except TransferException:
            return False, StateActionType.TRANSFER_EXP

    @property
    def start_state(self):
        return self._start_state

