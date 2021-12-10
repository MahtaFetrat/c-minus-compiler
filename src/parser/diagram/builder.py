import re

from src.parser.diagram.diagram import Diagram
from src.parser.diagram.state import State
from src.parser.diagram.transition import Transition
from src.parser.utils.enums import SymbolType


class Builder:
    def __init__(self, diagram_dict):
        self._diagram_dict = diagram_dict
        self._diagram = {}

        self._start_node = 0
        self._end_node = 1
        self._states = {}

    def build_transition_diagram(self):
        """Builds the transition diagram of the input dictionary of the transition diagram
        as a dictionary of Non-Terminal names and their Diagram object."""
        for rule in self._diagram_dict:
            self._build_rule_states(rule["states"])
            self._build_rule_diagram(rule)
        for rule in self._diagram_dict:
            self._build_rule_transitions(rule["transitions"])
        return self._diagram

    def _build_rule_states(self, states):
        for state in states:
            self._states[state["id"]] = State(state["id"], final=state["end"])
            if state["start"]:
                self._start_node = state["id"]
            if state["end"]:
                self._end_node = state["id"]

    def _build_rule_transitions(self, transitions):
        for tr in transitions:
            transition = Transition(
                dest=self._states[tr["state_dst_id"]],
                name=re.sub("_", "-", tr["name"]),
                symbol_type=SymbolType(tr["type"]),
                predicts=tr["predict"],
                follows=tr["follow"],
                diagram=self._diagram.get(tr["name"], None),
            )
            self._states[tr["state_src_id"]].add_transition(transition)

    def _build_rule_diagram(self, rule):
        self._diagram[rule["name"]] = Diagram(
            name=re.sub("_", "-", rule["name"]),
            start_state=self._states[self._start_node],
            final_state=self._states[self._end_node],
        )
