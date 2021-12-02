from typing import List

from src.base import Node
from src.scanner.utils.enums import TokenType, ErrorType
from src.scanner.dfa.transition import Transition


class State(Node):

    def __init__(self, state_id,
                 token_type: TokenType = TokenType.NONE,
                 error_type: ErrorType = ErrorType.NONE,
                 transitions: List[Transition] = None,
                 roll_back: bool = False):

        super().__init__(state_id, transitions)
        self._roll_back = roll_back or False
        self._token_type = token_type or TokenType.NONE
        self._error_type = error_type or ErrorType.NONE
        self.__cleanup__()

    def __cleanup__(self):
        if self._token_type != TokenType.NONE \
                and self._error_type != ErrorType.NONE:
            raise AttributeError('None error type with none final type is invalid')

    def transfer(self, character: str):
        try:
            state = list(filter(lambda x: x.is_valid(character), self._edges))[0].dest
            return state
        except IndexError:
            return InvalidState(self.identifier)

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
        return self._edges.copy()

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
