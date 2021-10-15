"""This module contains DFA graph elements classes."""

from enum import Enum


class DFA:
    """DFA graph."""

    def __init__(self, start_state):
        self.start_state = start_state


class State:
    """DFA graph node."""

    class TokenType(Enum):
        NONE = 0
        NUM = 1
        ID = 2
        KEYWORD = 3
        SYMBOL = 4
        COMMENT = 5
        WHITESPACE = 6

    def __init__(self, state_id, final=False, token_type=TokenType.NONE):
        self.state_id = state_id
        self.final = final
        self.token_type = token_type
        self.transitions = []

    def __eq__(self, other):
        return self.state_id == other.state_id

    def add_transition(self, transition):
        """Adds an outgoing edge to the node."""
        self.transitions.append(transition)


class Transition:
    """DFA graph edge."""

    def __init__(self, symbols, dest_state):
        self.symbols = symbols
        self.dest_state = dest_state

    def __eq__(self, other):
        return (
            set(self.symbols) == set(other.symbols)
            and self.dest_state == other.dest_state
        )
