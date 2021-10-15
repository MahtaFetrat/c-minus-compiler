"""This module provides tools for building a dfa as a graph."""

from src.scanner.dfa.dfa import DFA, State, Transition

# dfa dict output from https://github.com/vgarciasc/dfa-draw
dfa = {
    "alphabet": ["*", "9"],
    "states": [
        {
            "id": 0,
            "name": "0",
            "coord": {"x": 106, "y": 99},
            "radius": 20,
            "end": False,
            "start": True,
            "type": State.TokenType.NONE,
        },
        {
            "id": 1,
            "name": "1",
            "coord": {"x": 449, "y": 101},
            "radius": 20,
            "end": True,
            "start": False,
            "type": State.TokenType.NUM,
        },
    ],
    "transitions": [
        {"id": 0, "state_src_id": 0, "state_dst_id": 1, "symbols": ["9"]},
        {"id": 1, "state_src_id": 0, "state_dst_id": 0, "symbols": ["*"]},
        {"id": 2, "state_src_id": 1, "state_dst_id": 1, "symbols": ["9", "*"]},
    ],
}


def build_dfa(dfa_dict=dfa):
    """Returns the dfa built from the static dict above in this module."""
    start_state, states = build_states(dfa_dict)
    build_transitions(states, dfa_dict)
    return DFA(start_state)


def build_states(dfa_dict):
    """Returns the start node object and a dict of dfa state names to the state objects."""
    start_state = None
    states = {}
    for state in dfa_dict["states"]:
        new_state = State(state["id"], state["end"], state["type"])
        states[state["id"]] = new_state
        if state["start"]:
            start_state = new_state

    return start_state, states


def build_transitions(states, dfa_dict):
    """Builds the outgoing transitions for dfa states."""

    for transition in dfa_dict["transitions"]:
        new_transition = Transition(
            transition["symbols"], states[transition["state_dst_id"]]
        )
        states[transition["state_src_id"]].add_transition(new_transition)
