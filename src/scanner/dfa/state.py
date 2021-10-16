from typing import List

from src.scanner.utils.enums import TokenType
from src.scanner.dfa.transition import Transition
from src.scanner.utils.exceptions import TransferException, RoleBackException


class State(object):

    def __init__(self, state_id: int,
                 final: bool = False,
                 token_type=TokenType.NONE,
                 transitions: List[Transition] = None,
                 role_back: bool = False):
        self.state_id = state_id
        self.role_back = role_back

        self._transitions = transitions or []
        self._is_final = final
        self._token_type = token_type

    def __eq__(self, other):
        return bool(self.state_id == other.state_id)

    def __str__(self):
        return str(self.state_id)

    def transfer(self, character: str):
        try:
            state = list(filter(lambda x: x.is_valid(character), self._transitions))[0].dest_state
            if state.role_back and state.is_final():
                raise RoleBackException
            return state
        except IndexError:
            raise TransferException

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    def is_final(self) -> bool:
        return bool(self._is_final)

    @property
    def transitions(self):
        return self._transitions.copy()
