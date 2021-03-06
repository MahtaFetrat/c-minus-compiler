from src.base import EOF
from src.scanner.file_handler import FileHandler
from src.scanner.dfa import Builder, DFADict
from src.scanner.utils import TokenType, Language


class Scanner:
    def __init__(self, file):
        self._file_handler = FileHandler(file)
        self._dfa = Builder(DFADict()).build_dfa()

    @property
    def line_num(self):
        return self._file_handler.line_number

    def _get_next_terminal_state(self, current_state):
        """:raises StopIteration: if end of input file reached."""
        next_char = self._file_handler.get_next_char()
        if next_char == "\0" and current_state == self._dfa.start_state:
            raise StopIteration
        next_state = current_state.transfer(next_char)
        if not next_state.is_terminal():
            return self._get_next_terminal_state(next_state)
        if next_state.roll_back:
            self._file_handler.roll_back()
        return next_state

    def _write_next_terminal_state(self):
        """:raises StopIteration: if end of input file reached."""
        next_state = self._get_next_terminal_state(self._dfa.start_state)
        if next_state.is_error():
            return self._write_error_state(next_state)
        return self._write_final_state(next_state)

    def _write_error_state(self, state):
        line_num, lexeme = self._file_handler.get_lexeme(roll_back=state.roll_back)
        self._file_handler.write_error(line_num, lexeme, state.error_type.value)

    def _write_final_state(self, state):
        if state.token_type == TokenType.KEYID:
            return self._write_keyid_state(state)
        if state.token_type in [TokenType.NUM, TokenType.SYMBOL]:
            return self._write_non_keyid_state(state)
        _, _ = self._file_handler.get_lexeme(
            roll_back=state.roll_back
        )  # throw the lexeme away
        return None

    def _write_keyid_state(self, state):
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = "KEYWORD" if self._is_keyword(token_string) else "ID"
        self._file_handler.write_token(token_type, token_string)
        self._file_handler.write_symbol(token_string)
        return token_type, token_string

    def _write_non_keyid_state(self, state):
        _, token_string = self._file_handler.get_lexeme(roll_back=state.roll_back)
        token_type = state.token_type.name
        self._file_handler.write_token(token_type, token_string)
        return token_type, token_string

    @staticmethod
    def _is_keyword(token_string):
        return token_string in Language.KEYWORDS.value()

    def get_next_token(self):
        try:
            if next_token := self._write_next_terminal_state():
                return next_token
            return self.get_next_token()
        except StopIteration:
            return TokenType.SYMBOL.name, EOF

    def get_all_tokens(self):
        """Gets all tokens using the get_next_token method. Used for phase 1 test."""
        while True:
            _, token_string = self.get_next_token()
            if token_string == EOF:
                self.close()
                break

    def close(self):
        self._file_handler.close()
