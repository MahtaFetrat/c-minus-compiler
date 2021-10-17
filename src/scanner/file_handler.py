"""This module provides an interface for the scanner to work with I/O files."""


# pylint: disable=consider-using-with
class FileHandler:
    """This class provides an interface for reading the input and writing to the output files."""

    def __init__(self, input_filename="input.txt"):
        self._input_file = open(input_filename, "r", encoding="utf-8")

        self._buffer = self._input_file.readline()
        self._line_number = 1

        self._buffer_iterator = iter(self._buffer)
        self._lexeme = []
        self._lexeme_line_number = 1

        self._output_handler = OutputHandler()

    def get_next_char(self):
        """Gets the next character of the input file."""
        if not self._buffer:  # EOF encountered
            return "\0"
        try:
            next_char = next(self._buffer_iterator)
            self._update_lexeme(next_char)
            return next_char
        except StopIteration:
            self._proceed_to_next_line()
            self.get_next_char()

    def get_lexeme(self, rollback_character=False):
        """Returns the characters proceeded since the previous call to this function and
        the line number of the start of these characters."""
        lexeme = self._lexeme[: -1 if rollback_character else len(self._lexeme)]
        del self._lexeme[: -1 if rollback_character else len(self._lexeme)]
        if lexeme[:2] == ["/", "*"]:
            lexeme.append("...")
        return "".join(lexeme), self._lexeme_line_number

    def write_token(self, token_type, token_string):
        """Adds a token to the tokens file for the line of input currently being processed.
        Data will be flushed to the file at the end of the current line of input."""
        self._output_handler.add_token(token_type, token_string)

    def write_error(self, error_string, error_message):
        """Adds an error to the errors file for the line of input currently being processed.
        Data will be flushed to the file at the end of the current line of input."""
        self._output_handler.add_error(error_string, error_message)

    def write_symbol(self, symbol):
        """Adds a non-duplicate item to the symbol_table file. Data will be flushed to the file
        at a call to the close function of the object."""
        self._output_handler.add_symbol(symbol)

    def close(self):
        """Flushes data to the output files and closes all open files."""
        self._output_handler.close()
        self._input_file.close()

    def _proceed_to_next_line(self):
        """Writes the logs of the current line and reads a new line from the input file
        into the buffer."""
        self._output_handler.flush_buffers(self._line_number)
        self._buffer = self._input_file.readline()
        self._buffer_iterator = iter(self._buffer)
        self._line_number = self._line_number + 1

    def _update_lexeme(self, char):
        """Update the lexeme with the given character."""
        if len(self._lexeme) <= 1:
            self._lexeme_line_number = self._line_number

        self._lexeme.append(char)
        if self._lexeme[:2] == ["/", "*"]:
            self._lexeme = self._lexeme[:7]


class OutputHandler:
    """This class handles writing to the output files, including tokens, lexical_errors,
    and symbol_table, in a a buffered manner."""

    _LINE_LOG = "{}.\t{}\n"
    _ITEM_LOG = "({}, {}) "
    _TOKENS_FILENAME = "tokens.txt"
    _ERRORS_FILENAME = "lexical_errors.txt"
    _SYMBOL_TABLE_FILENAME = "symbol_table.txt"

    def __init__(self):
        self._tokens_file = open(OutputHandler._TOKENS_FILENAME, "w", encoding="utf-8")
        self._errors_file = open(OutputHandler._ERRORS_FILENAME, "w", encoding="utf-8")
        self._symbol_table = set()

        self._token_buffer = []
        self._error_buffer = []

    def add_token(self, token_type, token_string):
        """Adds a token to the tokens buffer which will be written in the tokens file."""
        self._token_buffer.append(
            OutputHandler._ITEM_LOG.format(token_type, token_string)
        )

    def add_error(self, error_string, error_message):
        """Adds an error log to the errors buffer which will be written in the errors file."""
        self._error_buffer.append(self._ITEM_LOG.format(error_string, error_message))

    def add_symbol(self, symbol):
        """Adds a non-duplicate item to the symbol table which will be written in the symbol table
        file."""
        self._symbol_table.add(symbol)

    def close(self):
        """Writes the symbol table to the output file and closes all open files."""
        self._write_symbol_table()
        self._tokens_file.close()
        self._errors_file.close()

    def flush_buffers(self, line_number):
        """Writes the buffered tokens and errors of the input line number to the output files."""
        self._flush_token_buffer(line_number)
        self._flush_error_buffer(line_number)

    def _flush_token_buffer(self, line_number):
        """Writes the buffered tokens of the input line number to the tokens file."""
        self._tokens_file.write(
            self._LINE_LOG.format(line_number, "".join(self._token_buffer))
        )
        self._token_buffer.clear()

    def _flush_error_buffer(self, line_number):
        """Writes the buffered errors of the input line number to the errors file."""
        self._errors_file.write(
            "".join(
                self._LINE_LOG.format(line_number, error)
                for error in self._error_buffer
            )
        )
        self._error_buffer.clear()

    def _write_symbol_table(self):
        """Writes the symbol table items to the symbol table file."""
        symbols = list(self._symbol_table)
        with open(
            OutputHandler._SYMBOL_TABLE_FILENAME, "w", encoding="utf-8"
        ) as symbol_table_file:
            symbol_table_file.write(
                "".join(
                    self._LINE_LOG.format(i, symbols[i])
                    for i in range(len(self._symbol_table))
                )
            )
