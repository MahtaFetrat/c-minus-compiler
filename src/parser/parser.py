from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.dict import TRANSITION_DIAGRAM
from src.scanner.scanner import Scanner


class Parser:
    START_STATE = "Program"

    def __init__(self, input_filename):
        self._scanner = Scanner(input_filename)
        self._transition_diagram = Builder(
            TRANSITION_DIAGRAM
        ).build_transition_diagram()

    def parse(self):
        diagram = self._transition_diagram[Parser.START_STATE]
        tree, _, _ = diagram.accept(self._scanner.get_next_token(), self._scanner)
        return tree
