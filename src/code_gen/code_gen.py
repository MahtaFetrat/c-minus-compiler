from typing import Dict, Any


class CodeGen:

    def __init__(self):
        self.semantic_stack = []
        self.routines: Dict[str, Any] = {
            '#declare_list': self.declare_func
        }

    def call(self, semantic_action, lookahead):
        self.routines[semantic_action](lookahead)

    def declare_func(self, lookahead=None):
        pass
