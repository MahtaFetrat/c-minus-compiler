import unittest

from src.scanner.dfa import build_dfa, State, StateActionType
from test.scanner.utils.dfa import DFA_TABLE


class TestDFA(unittest.TestCase):

    def setUp(self) -> None:
        self._simple_dfa = build_dfa(DFA_TABLE['simple'])
        self._keyid_dfa = build_dfa(DFA_TABLE['keyid'])

    def test_start_state(self):
        self.assertEqual(State(0), self._simple_dfa.start_state)
        self.assertEqual(State(0), self._keyid_dfa.start_state)

    def test_accept(self):
        self.assertEqual(self._simple_dfa.accepts("99*9e"),
                         (False, StateActionType.TRANSFER_EXP))
        self.assertEqual(self._simple_dfa.accepts("99*9"),
                         (True, StateActionType.REGULAR))
        self.assertEqual(self._keyid_dfa.accepts("a1b2c3"),
                         (False, StateActionType.UNFINISHED_EXP))
        self.assertEqual(self._keyid_dfa.accepts("a1b2/3\n"),
                         (False, StateActionType.TRANSFER_EXP))
        self.assertEqual(self._keyid_dfa.accepts("ab23ca\n"),
                         (True, StateActionType.ROLE_BACK))


if __name__ == "__main__":
    unittest.main()
