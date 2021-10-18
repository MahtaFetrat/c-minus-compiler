"""This module contains the scanner of c-minus language."""

from file_handler import FileHandler
from dfa.builder import build_dfa
from dfa.dfa_dict import DFA_DICT
from utils import TokenType


class Scanner:
    """The scanner of c-minus language."""

    KEYWORDS = ["if", "else", "void", "int", "repeat", "break", "until", "return"]

    def __init__(self):
        self._file_handler = FileHandler("input.txt")
        self._dfa = build_dfa(DFA_DICT)

    @property
    def line_num(self):
        """Returns the number of the line currently being processed by the scanner."""
        return self._file_handler.line_number

    def _get_next_terminal_state(self, current_state):
        """Returns the next terminal state, namely a final state or an error state."""
        next_state = current_state.transfer(self._file_handler.get_next_char())
        if next_state.final or next_state.error:
            if next_state.roll_back:
                self._file_handler.roll_back()
            return next_state
        return self._get_next_terminal_state(next_state)

    def _write_next_terminal_state(self):
        """Writes the next terminal state token or error to the output files and returns
        a tuple (token_type, token_string) if the state is related to a meaningful token,
        namely a NUM, SYMBOL, ID, or KEYWORD. Returns None otherwise."""
        next_state = self._get_next_terminal_state(self._dfa.start_state)
        if next_state.is_error:
            return self._write_error_state(next_state)
        return self._write_final_state(next_state)

    def _write_error_state(self, state):
        """Writes the state error to the output files."""
        line_num, lexeme = self._file_handler.get_lexeme(roll_back=state.role_back)
        self._file_handler.write_error(line_num, lexeme, state.error_type.value)

    def _write_final_state(self, state):
        """Writes the state token and returns the tuple (token_type, token_string) if
        the state is related to a meaningful token, namely a NUM, SYMBOL, ID, or KEYWORD.
        Returns None otherwise."""
        if state.token_type == TokenType.KEYID:
            return self._write_keyid_state(state)
        if state.token_type in [TokenType.NUM, TokenType.SYMBOL]:
            return self._write_non_keyid_state(state)
        return None

    def _write_keyid_state(self, state):
        """Writes the keyword or id token to the related output files and returns the tuple
        (token_type, token_string) in which the token_type is either ID or KEYWORD."""
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = "KEYWORD" if self._is_keyword(token_string) else "ID"
        self._file_handler.write_token(token_type, token_string)
        self._file_handler.write_symbol(token_string)
        return token_type, token_string

    def _write_non_keyid_state(self, state):
        """Writes the non-keyword or non-id tokens to the related output files and returns
        the tuple (token_type, token_string)."""
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = state.token_type.name
        self._file_handler.write_token(token_type, token_string)
        return token_type, token_string

    @staticmethod
    def _is_keyword(token_string):
        """Returns if a given token string is a registered keyword."""
        return token_string in Scanner.KEYWORDS

    def get_next_token(self):
        """Returns the next valid token of the input text."""
        if next_token := self._write_next_terminal_state():
            return next_token
        return self.get_next_token()
