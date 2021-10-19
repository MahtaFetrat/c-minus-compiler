from file_handler import FileHandler
from src.scanner.dfa import Builder
from src.scanner.utils.dfa import DFA_DICT
from utils import TokenType, Language


class Scanner:

    def __init__(self, file):
        self._file_handler = FileHandler(file)
        self._dfa = Builder(DFA_DICT).build_dfa()
        self._next_terminal_state = None

    @property
    def line_num(self):
        return self._file_handler.line_number

    def _get_next_terminal_state(self, current_state):
        next_state = current_state.transfer(self._file_handler.get_next_char())
        if next_state.is_terminal():
            if next_state.roll_back:
                self._file_handler.roll_back()
            self._next_terminal_state = next_state
            return next_state
        return self._get_next_terminal_state(next_state)

    def _write_next_terminal_state(self):
        next_state = self._get_next_terminal_state(self._dfa.start_state)
        if next_state.is_error():
            return self._write_error_state(next_state)
        return self._write_final_state(next_state)

    def _write_error_state(self, state):
        line_num, lexeme = self._file_handler.get_lexeme(roll_back=state.role_back)
        self._file_handler.write_error(line_num, lexeme, state.error_type.value)

    def _write_final_state(self, state):
        if state.token_type == TokenType.KEYID:
            return self._write_keyid_state(state)
        if state.token_type in [TokenType.NUM, TokenType.SYMBOL]:
            return self._write_non_keyid_state(state)
        return None

    def _write_keyid_state(self, state):
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = 'KEYWORD' if self._is_keyword(token_string) else 'ID'
        self._file_handler.write_token(token_type, token_string)
        self._file_handler.write_symbol(token_string)
        return token_type, token_string

    def _write_non_keyid_state(self, state):
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = state.token_type.name
        self._file_handler.write_token(token_type, token_string)
        return token_type, token_string

    def _flush_next_state_lexeme_errors(self):
        if self._next_terminal_state:
            self._next_terminal_state.flush_lexeme_errors()

    @staticmethod
    def _is_keyword(token_string):
        return token_string in Language.KEYWORDS.value()

    def get_next_token(self):
        if next_token := self._write_next_terminal_state():
            self._flush_next_state_lexeme_errors()
            return next_token
        return self.get_next_token()
