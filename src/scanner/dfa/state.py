from typing import List

from ..utils.enums import TokenType, ErrorType
from .transition import Transition


class State:

    def __init__(self, state_id,
                 token_type: TokenType = TokenType.NONE,
                 error_type: ErrorType = ErrorType.NONE,
                 transitions: List[Transition] = None,
                 roll_back: bool = False):

        self.state_id = state_id
        self._roll_back = roll_back or False
        self._transitions = transitions or []
        self._token_type = token_type or TokenType.NONE
        self._error_type = error_type or ErrorType.NONE
        self.__cleanup__()

    def __cleanup__(self):
        if self._token_type != TokenType.NONE \
                and self._error_type != ErrorType.NONE:
            raise AttributeError('None error type with none final type is invalid')

    def __eq__(self, other):
        return bool(self.state_id == other.state_id)

    def __str__(self):
        return str(self.state_id)

    def transfer(self, character: str):
        try:
            state = list(filter(lambda x: x.is_valid(character), self._transitions))[0].dest_state
            return state
        except IndexError:
            return InvalidState(self.state_id)

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    def is_final(self) -> bool:
        return self._token_type != TokenType.NONE

    def is_error(self) -> bool:
        return self._error_type != ErrorType.NONE

    def is_terminal(self) -> bool:
        return bool(self.is_final() or self.is_error())

    @property
    def roll_back(self):
        return self._roll_back

    @property
    def transitions(self):
        return self._transitions.copy()

    @property
    def token_type(self):
        return self._token_type

    @property
    def error_type(self):
        return self._error_type


class InvalidState(State):

    def __init__(self, state_id):
        super().__init__(
            state_id=state_id,
            error_type=ErrorType.INVALID_INPUT
        )

    def transfer(self, character: str):
        return self
