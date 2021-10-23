import re
import unittest
from src.scanner.scanner import Scanner


def read_symbol_table_file_as_set(content):
    return set(
        re.findall(
            r'\s+(.*)\n',
            content,
        )
    )


class TestScanner(unittest.TestCase):

    def assert_output_file_equal(self, test_number, file_name):
        with open(
                f'test_files/T{test_number}/{file_name}.txt', 'r', encoding='utf-8'
        ) as expected_file, open(f'{file_name}.txt', 'r', encoding='utf-8') as actual_file:
            expected_content = expected_file.read()
            actual_content = actual_file.read()
            self.assertEqual(expected_content, actual_content)

    def assert_symbol_table_equal(self, test_number):
        with open(
                f'test_files/T{test_number}/symbol_table.txt', 'r', encoding='utf-8'
        ) as expected_table_file, open(
            'symbol_table.txt', 'r', encoding='utf-8'
        ) as actual_table_file:
            expected_table_content = expected_table_file.read()
            expected_table_set = read_symbol_table_file_as_set(expected_table_content)
            actual_table_content = actual_table_file.read()
            actual_table_set = read_symbol_table_file_as_set(actual_table_content)
            self.assertEqual(expected_table_set, actual_table_set)

    def test_scanner_set1(self):
        for i in range(10):
            with self.subTest():
                test_number = f'{i + 1:02d}'
                scanner = Scanner(f'test_files/T{test_number}/input.txt')
                scanner.get_all_tokens()

                self.assert_output_file_equal(test_number, 'tokens')
                self.assert_output_file_equal(test_number, 'lexical_errors')
                self.assert_symbol_table_equal(test_number)

    def test_scanner_set2(self):
        # for i in range(10, 11):
        #     with self.subTest():
        i = 10
        test_number = f'{i + 1:02d}'
        scanner = Scanner(f'test_files/T{test_number}/input.txt')
        scanner.get_all_tokens()

        self.assert_output_file_equal(test_number, 'tokens')
        self.assert_output_file_equal(test_number, 'lexical_errors')
        self.assert_symbol_table_equal(test_number)


if __name__ == '__main__':
    unittest.main()
