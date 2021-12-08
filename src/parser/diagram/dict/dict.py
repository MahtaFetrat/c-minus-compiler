import re
from copy import deepcopy
from functools import reduce

from src.parser.diagram.dict.grammar import get_production_rules
from src.parser.utils import SymbolType

FOLLOW_SET = {
    "Program": ["\u0000"],
    "Declaration_list": [
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
    ],
    "Declaration": [
        "int",
        "void",
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
    ],
    "Declaration_initial": ["(", ";", "[", ",", ")"],
    "Declaration_prime": [
        "int",
        "void",
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
    ],
    "Var_declaration_prime": [
        "int",
        "void",
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
    ],
    "Fun_declaration_prime": [
        "int",
        "void",
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
    ],
    "Type_specifier": ["ID"],
    "Params": [")"],
    "Param_list": [")"],
    "Param": [",", ")"],
    "Param_prime": [",", ")"],
    "Compound_stmt": [
        "int",
        "void",
        "\u0000",
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Statement_list": ["}"],
    "Statement": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Expression_stmt": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Selection_stmt": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Else_stmt": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Iteration_stmt": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Return_stmt": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Return_stmt_prime": [
        "{",
        "break",
        ";",
        "if",
        "repeat",
        "return",
        "ID",
        "(",
        "NUM",
        "}",
        "endif",
        "else",
        "until",
    ],
    "Expression": [";", ")", "]", ","],
    "B": [";", ")", "]", ","],
    "H": [";", ")", "]", ","],
    "Simple_expression_zegond": [";", ")", "]", ","],
    "Simple_expression_prime": [";", ")", "]", ","],
    "C": [";", ")", "]", ","],
    "Relop": ["(", "ID", "NUM"],
    "Additive_expression": [";", ")", "]", ","],
    "Additive_expression_prime": ["<", "==", ";", ")", "]", ","],
    "Additive_expression_zegond": ["<", "==", ";", ")", "]", ","],
    "D": ["<", "==", ";", ")", "]", ","],
    "Addop": ["(", "ID", "NUM"],
    "Term": ["+", "-", ";", ")", "<", "==", "]", ","],
    "Term_prime": ["+", "-", "<", "==", ";", ")", "]", ","],
    "Term_zegond": ["+", "-", "<", "==", ";", ")", "]", ","],
    "G": ["+", "-", "<", "==", ";", ")", "]", ","],
    "Factor": ["*", "+", "-", ";", ")", "<", "==", "]", ","],
    "Var_call_prime": ["*", "+", "-", ";", ")", "<", "==", "]", ","],
    "Var_prime": ["*", "+", "-", ";", ")", "<", "==", "]", ","],
    "Factor_prime": ["*", "+", "-", "<", "==", ";", ")", "]", ","],
    "Factor_zegond": ["*", "+", "-", "<", "==", ";", ")", "]", ","],
    "Args": [")"],
    "Arg_list": [")"],
    "Arg_list_prime": [")"],
}
PREDICT_SET = {
    "1": ["int", "void", "\u0000"],
    "2": ["int", "void"],
    "3": ["\u0000", "{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM", "}"],
    "4": ["int", "void"],
    "5": ["int", "void"],
    "6": ["("],
    "7": [";", "["],
    "8": [";"],
    "9": ["["],
    "10": ["("],
    "11": ["int"],
    "12": ["void"],
    "13": ["int"],
    "14": ["void"],
    "15": [","],
    "16": [")"],
    "17": ["int", "void"],
    "18": ["["],
    "19": [",", ")"],
    "20": ["{"],
    "21": ["{", "break", ";", "if", "repeat", "return", "ID", "(", "NUM"],
    "22": ["}"],
    "23": ["break", ";", "ID", "(", "NUM"],
    "24": ["{"],
    "25": ["if"],
    "26": ["repeat"],
    "27": ["return"],
    "28": ["ID", "(", "NUM"],
    "29": ["break"],
    "30": [";"],
    "31": ["if"],
    "32": ["endif"],
    "33": ["else"],
    "34": ["repeat"],
    "35": ["return"],
    "36": [";"],
    "37": ["ID", "(", "NUM"],
    "38": ["(", "NUM"],
    "39": ["ID"],
    "40": ["="],
    "41": ["["],
    "42": ["(", "*", "+", "-", "<", "==", ";", ")", "]", ","],
    "43": ["="],
    "44": ["*", "+", "-", "<", "==", ";", ")", "]", ","],
    "45": ["(", "NUM"],
    "46": ["(", "*", "+", "-", "<", "==", ";", ")", "]", ","],
    "47": ["<", "=="],
    "48": [";", ")", "]", ","],
    "49": ["<"],
    "50": ["=="],
    "51": ["(", "ID", "NUM"],
    "52": ["(", "*", "+", "-", "<", "==", ";", ")", "]", ","],
    "53": ["(", "NUM"],
    "54": ["+", "-"],
    "55": ["<", "==", ";", ")", "]", ","],
    "56": ["+"],
    "57": ["-"],
    "58": ["(", "ID", "NUM"],
    "59": ["(", "*", "+", "-", "<", "==", ";", ")", "]", ","],
    "60": ["(", "NUM"],
    "61": ["*"],
    "62": ["+", "-", "<", "==", ";", ")", "]", ","],
    "63": ["("],
    "64": ["ID"],
    "65": ["NUM"],
    "66": ["("],
    "67": ["[", "*", "+", "-", ";", ")", "<", "==", "]", ","],
    "68": ["["],
    "69": ["*", "+", "-", ";", ")", "<", "==", "]", ","],
    "70": ["("],
    "71": ["*", "+", "-", "<", "==", ";", ")", "]", ","],
    "72": ["("],
    "73": ["NUM"],
    "74": ["ID", "(", "NUM"],
    "75": [")"],
    "76": ["ID", "(", "NUM"],
    "77": [","],
    "78": [")"],
}


class Dict:
    def __init__(self):
        self._transition_diagram = []
        self._state_id = 1
        self._production_rules = get_production_rules()

        self._start_state = 0
        self._final_state = 1
        self._states = []

    @staticmethod
    def get_nt_predict_set(non_terminal, production_rules_dict):
        production_rules = production_rules_dict[non_terminal]
        return Dict.sub_dollar_sign(
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
            Dict.get_nt_predict_set(name, self._production_rules)
            if name in FOLLOW_SET
            else Dict.sub_dollar_sign(PREDICT_SET.get(str(pr_no), {}))
            if name == "ε"
            else Dict.sub_dollar_sign([name])
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
            "predict_set": Dict.get_nt_predict_set(rule_name, self._production_rules),
            "follow_set": Dict.sub_dollar_sign(FOLLOW_SET[rule_name]),
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
