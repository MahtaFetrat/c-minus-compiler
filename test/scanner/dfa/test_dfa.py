import unittest

from src.scanner.dfa import build_dfa, State, StateActionType
from src.scanner.utils.dfa import dfa_dict
from test.scanner.utils.dfa import DFA_TABLE


class TestDFA(unittest.TestCase):

    def setUp(self) -> None:
        self._simple_dfa = build_dfa(DFA_TABLE['simple'])
        self._keyid_dfa = build_dfa(DFA_TABLE['keyid'])
        self._language_dfa = build_dfa(dfa_dict)

    def test_start_state(self):
        self.assertEqual(State(0), self._simple_dfa.start_state)
        self.assertEqual(State(0), self._keyid_dfa.start_state)
        self.assertEqual(State(0), self._language_dfa.start_state)

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

    def test_print(self):
        print(self._language_dfa)

    def test_language_dfa(self):
        # self.assertEqual(self._language_dfa.accepts("1234"),
        #                  (False, StateActionType.UNFINISHED_EXP))
        # self.assertEqual(self._language_dfa.accepts("1234="),
        #                  (True, StateActionType.ROLE_BACK))
        # self.assertEqual(self._language_dfa.accepts("an12n="),
        #                  (True, StateActionType.ROLE_BACK))
        # self.assertEqual(self._language_dfa.accepts("1234@"),
        #                  (False, StateActionType.TRANSFER_EXP))
        # self.assertEqual(self._language_dfa.accepts("1234n"),
        #                  (False, StateActionType.UNFINISHED_EXP))
        # self.assertEqual(self._language_dfa.accepts("=="),
        #                  (True, StateActionType.REGULAR))
        # self.assertEqual(self._language_dfa.accepts("*\\"),
        #                  (False, StateActionType.UNFINISHED_EXP))
        self.assertEqual(self._language_dfa.accepts("\\*ab*\\"),
                         (True, StateActionType.REGULAR))


if __name__ == "__main__":
    unittest.main()
