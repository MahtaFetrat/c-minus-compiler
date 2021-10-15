import re
import unittest
from src.scanner.utils.file_handler import FileHandler


def read_symbol_table_file_as_set(content):
    return set(
        re.findall(
            r"\s+(.*)\n",
            content,
        )
    )


class TestFileHandler(unittest.TestCase):
    def test_next_char(self):
        file_handler = FileHandler()
        self.assertEqual(file_handler.get_next_char(), "h")
        self.assertEqual(file_handler.get_next_char(), "e")
        file_handler.close()

    def test_get_lexeme(self):
        file_handler = FileHandler()
        for _ in "hello":
            file_handler.get_next_char()
        self.assertEqual(file_handler.get_lexeme(), "hello")

        file_handler.get_next_char()
        file_handler.get_lexeme()

        for _ in "world":
            file_handler.get_next_char()
        self.assertEqual(file_handler.get_lexeme(), "world")
        file_handler.close()

    def test_get_multiline_lexeme(self):
        file_handler = FileHandler()
        for _ in "hello world\nin the next line":
            file_handler.get_next_char()
        self.assertEqual(file_handler.get_lexeme(), "hello world\n")
        file_handler.close()

    def test_write_token(self):
        file_handler = FileHandler()
        for _ in "hello world\n":
            file_handler.get_next_char()
        file_handler.write_token("KEYWORD", "void")
        file_handler.write_token("ID", "main")
        file_handler.write_token("SYMBOL", "(")
        file_handler.write_error("3d", "Invalid number")
        file_handler.write_error("cd!", "Invalid input")

        for _ in "in the next line\n":
            file_handler.get_next_char()
        file_handler.write_token("KEYWORD", "int")
        file_handler.write_token("ID", "a")
        file_handler.write_token("SYMBOL", "=")
        file_handler.write_error("*/", "Unmatched comment")

        file_handler.get_next_char()
        file_handler.close()

        with open("tokens.txt", "r", encoding="utf-8") as file:
            content = file.read()
            self.assertEqual(
                content,
                "1.\t(KEYWORD, void) (ID, main) (SYMBOL, () \n"
                + "2.\t(KEYWORD, int) (ID, a) (SYMBOL, =) \n",
            )

        with open("lexical_errors.txt", "r", encoding="utf-8") as file:
            content = file.read()
            self.assertEqual(
                content,
                "1.\t(3d, Invalid number) \n1.\t(cd!, Invalid input) \n"
                + "2.\t(*/, Unmatched comment) \n",
            )

    def test_write_symbol(self):
        file_handler = FileHandler()
        file_handler.write_symbol("if")
        file_handler.write_symbol("a")
        file_handler.write_symbol("main")
        file_handler.write_symbol("else")
        file_handler.write_symbol("if")
        file_handler.write_symbol("main")
        file_handler.write_symbol("cde")

        file_handler.close()

        with open("symbol_table.txt", "r", encoding="utf-8") as file:
            content = file.read()
            symbol_table = read_symbol_table_file_as_set(content)
            self.assertEqual(symbol_table, {"if", "a", "main", "else", "cde"})


if __name__ == "__main__":
    unittest.main()
