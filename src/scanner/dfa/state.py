from typing import List

from src.scanner.utils.enums import TokenType, ErrorType, Language
from src.scanner.dfa.transition import Transition
from src.scanner.utils.exceptions import TransferException


class State(object):

    def __init__(self, state_id: int,
                 final: bool = False,
                 error: bool = False,
                 token_type: TokenType = TokenType.NONE,
                 error_type: ErrorType = ErrorType.NONE,
                 transitions: List[Transition] = None,
                 role_back: bool = False):

        self.state_id = state_id
        self.role_back = role_back or False
        self._transitions = transitions or []
        self._final = final or False
        self._error = error or False
        self._token_type = token_type or TokenType.NONE
        self._error_type = error_type or TokenType.NONE
        self.__cleanup__()

    def __cleanup__(self):
        if self._token_type != TokenType.NONE and not self._final:
            raise AssertionError('Token type vs final is required')
        if self._token_type == TokenType.NONE and self._final:
            raise AssertionError('Token type vs final is required')
        if self._final and self._error:
            raise AssertionError('Error vs final is invalid')

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

    def is_final(self) -> bool:
        return bool(self._final)

    def is_error(self) -> bool:
        return bool(self._error)

    @property
    def transitions(self):
        return self._transitions.copy()

    @property
    def token_type(self, lexeme=None):
        if not hasattr(self, '_final'):
            raise AttributeError('State is not final.')

        if self._token_type == TokenType.KEYID:
            if lexeme is None:
                raise AttributeError('Lexeme for key id type is mandatory.')

            if self._token_type in Language.KEYWORD.value:
                return TokenType.KEYWORD
            return TokenType.ID

        return self._token_type

    @property
    def error_type(self):
        return self._error_type
