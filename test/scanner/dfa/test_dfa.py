import unittest

from src.scanner.dfa import build_dfa, State, RoleBackException
from test.scanner.utils.dfa import DFA_TABLE


class TestDFA(unittest.TestCase):

    def setUp(self) -> None:
        self._simple_dfa = build_dfa(DFA_TABLE['simple'])
        self._keyid_dfa = build_dfa(DFA_TABLE['keyid'])

    def test_start_state(self):
        self.assertEqual(State(0), self._simple_dfa.start_state)
        self.assertEqual(State(0), self._keyid_dfa.start_state)

    def test_accept(self):
        self.assertFalse(self._simple_dfa.accepts("99*9e"))
        self.assertTrue(self._simple_dfa.accepts("99*9"))
        self.assertFalse(self._keyid_dfa.accepts("a1b2c3"))
        self.assertFalse(self._keyid_dfa.accepts("a1b2/3\n"))
        self.assertRaises(RoleBackException,
                          self._keyid_dfa.accepts.__func__,
                          self._keyid_dfa,
                          "ab23c a\n")


if __name__ == "__main__":
    unittest.main()
