"""This module provides tools for building a dfa as a graph."""

from src.scanner.dfa import State, Transition
from src.scanner.dfa.dfa import DFA


# dfa dict output from https://github.com/vgarciasc/dfa-draw
dfa = {}


def build_dfa(dfa_dict=None):
    """Returns the dfa built from the static dict above in this module."""
    dfa_dict = dfa_dict or dfa
    start_state, states = _build_states(dfa_dict)
    _build_transitions(states, dfa_dict)
    return DFA(start_state)


def _build_states(dfa_dict):
    """Returns the start node object and a dict of dfa state names to the state objects."""
    start_state = None
    states = {}
    for state in dfa_dict['states']:
        new_state = State(state_id=state['id'],
                          final=state.get('end'),
                          token_type=state.get('type'),
                          role_back=state.get('role_back'),
                          error=state.get('error'))
        states[state['id']] = new_state
        if state.get('start'):
            start_state = new_state

    return start_state, states


def _build_transitions(states, dfa_dict):
    """Builds the outgoing transitions for dfa states."""

    for transition in dfa_dict['transitions']:
        new_transition = Transition(
            transition['symbols'], states[transition['state_dst_id']]
        )
        states[transition['state_src_id']].add_transition(new_transition)
