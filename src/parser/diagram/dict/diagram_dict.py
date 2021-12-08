import re
from copy import deepcopy
from functools import reduce

from src.parser.diagram.dict.grammar import get_production_rules
from src.parser.utils import SymbolType
from src.parser.utils import FOLLOW_SET, PREDICT_SET


class DiagramDict:
    def __init__(self):
        self._transition_diagram = []
        self._state_id = 1
        self._production_rules = get_production_rules()

        self._start_state = 0
        self._final_state = 1
        self._states = []

    @property
    def state_id(self):
        return self._state_id

    @staticmethod
    def get_nt_predict_set(non_terminal, production_rules_dict):
        production_rules = production_rules_dict[non_terminal]
        return DiagramDict.sub_dollar_sign(
            reduce(
                lambda x, y: x.union(set(y)),
                [
                    PREDICT_SET[str(production_no)]
                    for production_no, _ in production_rules
                ],
                set(),
            )
        )

    @staticmethod
    def sub_dollar_sign(predict_list):
        return [re.sub("\u0000", "$", re.sub("┤", "$", x)) for x in predict_list]

    @staticmethod
    def _get_transition_type(name):
        return (
            SymbolType.NON_TERMINAL.value
            if name in FOLLOW_SET
            else SymbolType.EPSILON.value
            if name == "ε"
            else SymbolType.TERMINAL.value
        )

    def _get_transition_predict(self, name, pr_no):
        return (
            DiagramDict.get_nt_predict_set(name, self._production_rules)
            if name in FOLLOW_SET
            else DiagramDict.sub_dollar_sign(PREDICT_SET.get(str(pr_no), {}))
            if name == "ε"
            else DiagramDict.sub_dollar_sign([name])
        )

    def _build_transition_dict(
        self, name, start_state_id, dest_state_id, production_rule_no
    ):
        return {
            "state_src_id": start_state_id,
            "state_dst_id": dest_state_id,
            "type": self._get_transition_type(name),
            "name": re.sub("┤", "$", name),
            "predict": self._get_transition_predict(name, production_rule_no),
        }

    def _build_rule_transitions(self, production_rules):
        transitions = []
        for production_rule_no, production_rule_words in production_rules:
            previous_state_id = self._start_state["id"]
            for transition_no, transition_name in enumerate(production_rule_words):
                dest_state_id = (
                    self._states.pop(0)["id"]
                    if transition_no != len(production_rule_words) - 1
                    else self._final_state["id"]
                )
                transitions.append(
                    self._build_transition_dict(
                        transition_name,
                        previous_state_id,
                        dest_state_id,
                        production_rule_no,
                    )
                )
                previous_state_id = dest_state_id
        return transitions

    def _build_rule_states(self, production_rules):
        self._start_state = {"id": self._state_id, "start": True, "end": False}
        self._final_state = {"id": self._state_id + 1, "start": False, "end": True}
        self._state_id += 2
        for _, production_rule_words in production_rules:
            for state in range(len(production_rule_words) - 1):
                self._states.append(
                    {"id": self._state_id, "start": False, "end": False}
                )
                self._state_id += 1
        return deepcopy([self._start_state, self._final_state] + self._states)

    def _build_rule_diagram_dict(self, rule_name, production_rules):
        diagram = {
            "name": rule_name,
            "predict_set": DiagramDict.get_nt_predict_set(rule_name, self._production_rules),
            "follow_set": DiagramDict.sub_dollar_sign(FOLLOW_SET[rule_name]),
            "states": self._build_rule_states(production_rules),
            "transitions": self._build_rule_transitions(production_rules),
        }
        self._transition_diagram.append(diagram)

    def _build_transition_diagram_dict(self):
        for rule_name, production_rules in self._production_rules.items():
            self._states = []
            self._build_rule_diagram_dict(rule_name, production_rules)

    def get_transition_diagram_dict(self):
        """Returns a dictionary of the transition diagram for the grammar in grammar.py"""
        if not self._transition_diagram:
            self._build_transition_diagram_dict()
        return self._transition_diagram
