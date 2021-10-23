"""This module provides an interface for the scanner to work with I/O files."""

from src.scanner.utils.enums import Language


# pylint: disable=consider-using-with
class FileHandler:
    """This class provides an interface for reading the input and writing to the output files."""

    def __init__(self, file):
        self._input_file = open(file, "r", encoding="utf-8")

        self._buffer = ""
        self._line_number = 0

        self._buffer_iterator = Iterator(self._buffer)

        self._lexeme = []
        self._lexeme_line_number = 1

        self._output_handler = OutputHandler()

        self._proceed_to_next_line()

    def get_next_char(self):
        """Gets the next character of the input file."""
        if not self._buffer:  # EOF encountered
            self._output_handler.flush_buffers(self._line_number)
            self._update_lexeme("\0")
            return "\0"
        try:
            next_char = next(self._buffer_iterator)
            self._update_lexeme(next_char)
            return next_char
        except StopIteration:
            self._proceed_to_next_line()
            return self.get_next_char()

    def get_lexeme(self, roll_back=False):
        """Returns a tuple (the line number of the start of the lexeme,
        the characters proceeded since the previous call to this function)."""
        lexeme = self._lexeme[: -1 if roll_back else len(self._lexeme)]
        self._lexeme.clear()
        if lexeme[:2] == ["/", "*"]:
            lexeme.append("...")
        return self._lexeme_line_number, "".join(lexeme)

    def write_token(self, token_type, token_string):
        """Adds a token to the tokens file for the line of input currently being processed.
        Data will be flushed to the file at the end of the current line of input."""
        self._output_handler.add_token(token_type, token_string)

    def write_error(self, line_number, error_string, error_message):
        """Adds an error to the errors file for the line of input currently being processed.
        Data will be flushed to the file at the end of the current line of input."""
        self._output_handler.add_error(line_number, error_string, error_message)

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
        if self._buffer and self._buffer[-1] != "\n":  # Add final new-line
            self._buffer = self._buffer + "\n"
        self._buffer_iterator = Iterator(self._buffer)
        self._line_number += 1 if self._buffer else 0

    def _update_lexeme(self, char):
        """Update the lexeme with the given character."""
        if len(self._lexeme) <= 1:
            self._lexeme_line_number = self._line_number

        self._lexeme.append(char)
        if self._lexeme[:2] == ["/", "*"]:
            self._lexeme = self._lexeme[:7]

    @property
    def line_number(self):
        """Returns the number of the line currently being processed by the scanner file handler."""
        return self._line_number

    def roll_back(self):
        """Moves the iterator one character back. Note that iterator can move back at most
        one character and using this function multiple times has no further effect."""
        self._buffer_iterator.roll_back()


class Iterator:
    """Custom iterator with one character history."""

    def __init__(self, buffer):
        self._iterator = iter(buffer)
        self._history = ""
        self._roll_back = False

    def __next__(self):
        if self._roll_back:
            self._roll_back = False
            return self._history
        self._history = next(self._iterator)
        return self._history

    def roll_back(self):
        """Moves the iterator one character back. Note that iterator can move back at most
        one character and using this function multiple times has no further effect."""
        self._roll_back = True


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
        self._symbol_table = set(Language.KEYWORDS.value())

        self._token_buffer = []
        self._error_buffer = []
        self._error_line_number = 1
        self._error_found = False

    def add_token(self, token_type, token_string):
        """Adds a token to the tokens buffer which will be written in the tokens file."""
        self._token_buffer.append(
            OutputHandler._ITEM_LOG.format(token_type, token_string)
        )

    def add_error(self, line_number, error_string, error_message):
        """Adds an error log to the errors buffer which will be written in the errors file."""
        self._error_found = True
        self._error_line_number = line_number
        self._error_buffer.append(
            OutputHandler._ITEM_LOG.format(error_string, error_message)
        )

    def add_symbol(self, symbol):
        """Adds a non-duplicate item to the symbol table which will be written in the symbol table
        file."""
        self._symbol_table.add(symbol)

    def close(self):
        """Writes the symbol table to the symbol_table.txt file.
        Writes 'There is no lexical error.' in the lexical_errors.txt if no errors were found.
        And closes all open files."""
        self._write_symbol_table()
        self._tokens_file.close()
        self._close_error_file()

    def flush_buffers(self, line_number):
        """Writes the buffered tokens and errors of the input line number to the output files."""
        self._flush_token_buffer(line_number)
        self._flush_error_buffer()

    def _flush_token_buffer(self, line_number):
        """Writes the buffered tokens of the input line number to the tokens file."""
        if self._token_buffer:
            self._tokens_file.write(
                self._LINE_LOG.format(line_number, "".join(self._token_buffer))
            )
        self._token_buffer.clear()

    def _flush_error_buffer(self):
        """Writes the buffered errors of the input line number to the errors file."""
        if self._error_buffer:
            self._errors_file.write(
                self._LINE_LOG.format(
                    self._error_line_number, "".join(self._error_buffer)
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

    def _close_error_file(self):
        """Writes 'There is no lexical error.' in the lexical_errors.txt if no errors were found.
        And closes the file."""
        if not self._error_found:
            self._errors_file.write("There is no lexical error.")
        self._errors_file.close()
