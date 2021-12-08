from src.parser.diagram.diagram import Diagram
from src.parser.diagram.state import State
from src.parser.diagram.transition import Transition
from src.parser.utils.enums import SymbolType


class Builder:
    def __init__(self, diagram_dict):
        self._diagram_dict = diagram_dict
        self._diagram = {}
        self._states = {}

    def build_transition_diagram(self):
        for rule in self._diagram_dict:
            self._build_rule_states(rule["states"])
            self._build_rule_diagram(rule)
        for rule in self._diagram_dict:
            self._build_rule_transitions(rule["transitions"])
        return self._diagram

    def _build_rule_states(self, states):
        for state in states:
            self._states[state["id"]] = State(
                identifier=state["id"], final=state["end"]
            )

    def _build_rule_transitions(self, transitions):
        for tr in transitions:
            transition = Transition(
                dest=self._states[tr["state_dst_id"]],
                name=tr["name"],
                symbol_type=SymbolType(tr["type"]),
                predicts=tr["predict"],
                diagram=self._diagram.get(tr["name"], None),
            )
            self._states[tr["state_src_id"]].add_transition(transition)

    def _build_rule_diagram(self, rule):
        for state in rule["states"]:
            if state["start"]:
                self._diagram[rule["name"]] = Diagram(
                    name=rule["name"], start_node=self._states[state["id"]]
                )
