from typing import List

from src.scanner.utils.enums import TokenType, ErrorType
from src.scanner.dfa.transition import Transition
from src.scanner.utils.exceptions import TransferException


class State(object):

    def __init__(self, state_id: int,
                 final: bool = False,
                 error: bool = False,
                 token_type=TokenType.NONE,
                 error_type=ErrorType.NONE,
                 transitions: List[Transition] = None,
                 role_back: bool = False):
        self.state_id = state_id
        self.role_back = role_back

        self._transitions = transitions or []
        self._is_final = final
        self._is_error = error
        self._token_type = token_type
        self._error_type = error_type

    def __eq__(self, other):
        return bool(self.state_id == other.state_id)

    def __str__(self):
        return str(self.state_id)

    def transfer(self, character: str):
        try:
            state = list(filter(lambda x: x.is_valid(character), self._transitions))[0].dest_state
            return state
        except IndexError:
            raise TransferException

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    @property
    def is_final(self) -> bool:
        return bool(self._is_final)

    @property
    def is_error(self) -> bool:
        return bool(self._is_error)

    @property
    def token_type(self):
        return self._token_type

    @property
    def error_type(self):
        return self._error_type

    @property
    def transitions(self):
        return self._transitions.copy()
