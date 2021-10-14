"""This module provides an interface for the scanner to work with I/O files."""


class FileHandler:
    """This class provides an interface for reading the input text file,
    and writing to the output files, including tokens, lexical_errors, and symbol_table."""

    _LINE_LOG = "{}.\t"
    _ITEM_LOG = "({}, {})"

    def __init__(self, input_filename):
        self._input_file = open(input_filename, "r", encoding="utf-8")
        self._tokens_file = open("tokens.txt", "w", encoding="utf-8")
        self._errors_file = open("lexical_errors.txt", "w", encoding="utf-8")
        self._symbol_table = set()

        self._buffer = self._input_file.readline()
        self._line_number = 1

        self._iterator = iter(self._buffer)
        self._lexeme = bytearray()

        self._token_buffer = []
        self._error_buffer = []

    def get_next_char(self):
        """Gets the next character of the input.txt file."""
        if not (next_char := next(self._iterator)):
            self._proceed_to_next_line()
            next_char = next(self._iterator)
        self._extend_lexeme(next_char)
        return next_char

    def get_lexeme(self):
        """Returns the characters proceeded since the previous call to this function."""
        lexeme = self._lexeme[:]
        self._lexeme.clear()
        return lexeme

    def write_token(self, token_type, token_string):
        """Adds a token to the tokens buffer to be written in tokens.txt file."""
        self._token_buffer.append(self._ITEM_LOG.format(token_type, token_string))

    def write_error(self, error_string, error_message):
        """Adds an error log to the errors buffer to be written in lexical_errors.txt file."""
        self._error_buffer.append(
            self._LINE_LOG.format(
                self._line_number, self._ITEM_LOG.format(error_string, error_message)
            )
        )

    def write_symbol(self, symbol):
        """Adds an item to the symbol table which will be written in symbol_table.txt."""
        self._symbol_table.add(symbol)

    def close(self):
        """Writes the symbol table to file and closes all open files."""
        self._write_symbol_table()
        self._input_file.close()
        self._tokens_file.close()
        self._errors_file.close()

    def _proceed_to_next_line(self):
        """Writes the logs of the current line and reads a new line from the input file
        into the buffer."""
        self._flush_buffers()
        self._buffer = self._input_file.readline()
        self._iterator = iter(self._buffer)
        self._line_number = self._line_number + 1

    def _extend_lexeme(self, char):
        """Appends the newly read character to the lexeme so far."""
        if self._lexeme[-1] != "\n":
            self._lexeme.append(char)

    def _flush_buffers(self):
        """Writes the buffered tokens and errors of the current line to the output files."""
        self._flush_token_buffer()
        self._flush_error_buffer()

    def _flush_token_buffer(self):
        """Writes the buffered tokens of the current line to the output files."""
        self._tokens_file.write(
            self._LINE_LOG.format(self._line_number, " ".join(self._token_buffer))
        )

    def _flush_error_buffer(self):
        """Writes the buffered errors of the current line to the output files."""
        self._errors_file.write("\n".join(self._error_buffer))

    def _write_symbol_table(self):
        """Writes the keywords and ids to symbol_table.txt."""
        symbols = list(self._symbol_table)
        with open("symbol_table.txt", "w", encoding="utf-8") as symbol_table_file:
            symbol_table_file.write(
                "\n".join(
                    self._LINE_LOG.format(i, symbols[i])
                    for i in range(len(self._symbol_table))
                )
            )
