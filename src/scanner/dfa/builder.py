"""This module provides tools for building a dfa as a graph."""

from .state import State
from .transition import Transition
from .dfa import DFA


def build_dfa(dfa_dict):
    """Returns the dfa built from the static dict above in this module."""
    start_state, states = build_states(dfa_dict)
    build_transitions(states, dfa_dict)
    return DFA(start_state)


def build_states(dfa_dict):
    """Returns the start node object and a dict of dfa state names to the state objects."""
    start_state = None
    states = {}
    for state in dfa_dict["states"]:
        new_state = State(
            state_id=state["id"],
            final=state["end"],
            token_type=state.get("type"),
            role_back=state.get("role_back"),
        )
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
