import unittest
from src.scanner.dfa.builder import Builder
from src.scanner.dfa import State, Transition
from test.scanner.utils.dfa import SIMPLE_DFA_DICT


class TestBuilder(unittest.TestCase):

    def test_build_dfa_start(self):
        dfa = Builder(SIMPLE_DFA_DICT).build_dfa()
        self.assertEqual(State(0), dfa.start_state)

    def test_build_dfa_transitions(self):
        dfa = Builder(SIMPLE_DFA_DICT).build_dfa()
        transitions = dfa.start_state.transitions
        self.assertIn(Transition(["1"], State(0)), transitions)
        self.assertIn(Transition(["9"], State(1)), transitions)

        final_state_transitions = dfa.start_state.transitions[0].dest_state
        self.assertIn(
            Transition(["1", "9"], State(1)), final_state_transitions.transitions
        )


if __name__ == "__main__":
    unittest.main()
