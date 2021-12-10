import unittest

from src.parser.parser import Parser


class TestParser(unittest.TestCase):
    def assert_output_file_equal(self, test_number, file_name):
        with open(
            f"test_files/T{test_number}/{file_name}.txt", "r", encoding="utf-8"
        ) as expected_file, open(
            f"{file_name}.txt", "r", encoding="utf-8"
        ) as actual_file:
            expected_content = expected_file.read()
            actual_content = actual_file.read()
            self.assertEqual(expected_content, actual_content)

    def test_parse_set1(self):
        for i in range(10):
            with self.subTest():
                test_number = f"{i + 1:02d}"
                parser = Parser(f"test_files/T{test_number}/input.txt")
                parser.parse()

        self.assert_output_file_equal(test_number, "parse_tree")
        self.assert_output_file_equal(test_number, "syntax_errors")

    def test_parse_set2(self):
        for i in range(10, 20):
            with self.subTest():
                test_number = f"{i + 1:02d}"
                parser = Parser(f"test_files/T{test_number}/input.txt")
                parser.parse()

        self.assert_output_file_equal(test_number, "parse_tree")
        self.assert_output_file_equal(test_number, "syntax_errors")


if __name__ == "__main__":
    unittest.main()
