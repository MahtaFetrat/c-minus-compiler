import unittest
from src.scanner.dfa.builder import build_dfa
from src.scanner.dfa import State, Transition
from test.scanner.utils.dfa import simple_dfa_dict


class TestBuilder(unittest.TestCase):

    def test_build_dfa_start(self):
        dfa = build_dfa(simple_dfa_dict)
        self.assertEqual(State(0), dfa.start_state)

    def test_build_dfa_transitions(self):
        dfa = build_dfa(simple_dfa_dict)
        transitions = dfa.start_state.transitions
        self.assertIn(Transition(["*"], State(0)), transitions)
        self.assertIn(Transition(["9"], State(1, True)), transitions)

        final_state_transitions = dfa.start_state.transitions[0].dest_state
        self.assertIn(
            Transition(["*", "9"], State(1)), final_state_transitions.transitions
        )


if __name__ == "__main__":
    unittest.main()
