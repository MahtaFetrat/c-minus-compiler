import unittest

from src.scanner.dfa import Builder, State, ErrorType, TokenType, DFADict
from test.scanner.utils.dfa import SIMPLE_DFA_DICT, KEYID_DFA_DICT


class TestDFA(unittest.TestCase):

    def setUp(self) -> None:
        self._simple_dfa = Builder(SIMPLE_DFA_DICT).build_dfa()
        self._keyid_dfa = Builder(KEYID_DFA_DICT).build_dfa()
        self._language_dfa = Builder(DFADict()).build_dfa()

    def test_start_state(self):
        self.assertEqual(State(0), self._simple_dfa.start_state)
        self.assertEqual(State(0), self._keyid_dfa.start_state)
        self.assertEqual(State(0), self._language_dfa.start_state)

    def test_iterate_simple_dfa(self):
        self.assert_terminal_is_final(self._simple_dfa, '9199', False, TokenType.NUM, 1)
        self.assert_terminal_is_error(self._simple_dfa, '9199e', ErrorType.INVALID_INPUT, 1)

    def test_iterate_keyid_dfa(self):
        self.assert_terminal_is_final(self._keyid_dfa, 'a1b2c3=', True, TokenType.KEYID, 2)
        self.assert_terminal_is_error(self._keyid_dfa, 'a1b2@', ErrorType.INVALID_INPUT, 1)

    def test_language_dfa(self):
        self.assert_terminal_is_final(self._language_dfa, 'a1b2 ', True, TokenType.KEYID, 5)
        self.assert_terminal_is_final(self._language_dfa, '/*ab*/', False, TokenType.COMMENT, 17)
        self.assert_terminal_is_final(self._language_dfa, '==', False, TokenType.SYMBOL, 12)
        self.assert_terminal_is_final(self._language_dfa, '// ab \n', True, TokenType.COMMENT, 19)
        self.assert_terminal_is_error(self._language_dfa, '/*ab\0', ErrorType.UNCLOSED_COMMENT, 20)
        self.assert_terminal_is_error(self._language_dfa, '*/', ErrorType.UNMATCHED_COMMENT, 7)
        self.assert_terminal_is_error(self._language_dfa, '12@', ErrorType.INVALID_NUMBER, 3)
        self.assert_terminal_is_error(self._language_dfa, '12d', ErrorType.INVALID_NUMBER, 3)
        self.assert_terminal_is_error(self._language_dfa, '*@', ErrorType.INVALID_INPUT, 6)

    def assert_terminal_is_final(self, dfa, string, roll_back, token_type, dest_id):
        dfa.iterate(string)
        self.assertEqual(dfa.terminal_state, State(dest_id))
        self.assertFalse(dfa.terminal_state.is_error())
        self.assertTrue(dfa.terminal_state.is_final())
        self.assertEqual(dfa.terminal_state.roll_back, roll_back)
        self.assertEqual(dfa.terminal_state.token_type, token_type)

    def assert_terminal_is_error(self, dfa, string, error_type, dest_id):
        dfa.iterate(string)
        self.assertEqual(dfa.terminal_state, State(dest_id))
        self.assertTrue(dfa.terminal_state.is_error())
        self.assertEqual(dfa.terminal_state.error_type, error_type)


if __name__ == '__main__':
    unittest.main()
