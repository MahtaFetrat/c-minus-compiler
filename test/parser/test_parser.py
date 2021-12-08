import unittest

from src.parser import Parser


class TestParser(unittest.TestCase):

    def test_parse(self):
        parser = Parser(f'test_files/T01/input.txt')
        tree = parser.parse()
        print(tree.get_printable_tree())



if __name__ == '__main__':
    unittest.main()
