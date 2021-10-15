import unittest
from src.scanner.dfa.builder import build_dfa
from src.scanner.dfa import State, Transition
from src.scanner.utils.enums import TokenType

dfa_dict = {
    "alphabet": ["*", "9"],
    "states": [
        {
            "id": 0,
            "name": "0",
            "coord": {"x": 106, "y": 99},
            "radius": 20,
            "end": False,
            "start": True,
            "type": TokenType.NONE,
        },
        {
            "id": 1,
            "name": "1",
            "coord": {"x": 449, "y": 101},
            "radius": 20,
            "end": True,
            "start": False,
            "type": TokenType.NUM,
        },
    ],
    "transitions": [
        {"id": 0, "state_src_id": 0, "state_dst_id": 1, "symbols": ["9"]},
        {"id": 1, "state_src_id": 0, "state_dst_id": 0, "symbols": ["*"]},
        {"id": 2, "state_src_id": 1, "state_dst_id": 1, "symbols": ["9", "*"]},
    ],
}


class TestBuilder(unittest.TestCase):

    def test_build_dfa_start(self):
        dfa = build_dfa(dfa_dict)
        self.assertEqual(State("0"), dfa.start_state)

    def test_build_dfa_transitions(self):
        dfa = build_dfa(dfa_dict)
        transitions = dfa.start_state.transitions
        self.assertIn(Transition(["*"], State("0")), transitions)
        self.assertIn(Transition(["9"], State("1", True)), transitions)

        final_state_transitions = dfa.start_state.transitions[0].dest_state
        self.assertIn(
            Transition(["*", "9"], State("1")), final_state_transitions.transitions
        )


if __name__ == "__main__":
    unittest.main()
