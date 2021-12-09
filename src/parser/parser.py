from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.diagram_dict import DiagramDict
from src.parser.utils import ParseException, MissingException
from src.scanner.scanner import Scanner


class Parser:
    START_STATE = "Program"

    def __init__(self, input_filename):
        self._scanner = Scanner(input_filename)
        self._transition_diagram = Builder(
            DiagramDict().get_transition_diagram_dict()
        ).build_transition_diagram()

    def parse(self):
        diagram = self._transition_diagram[Parser.START_STATE]
        # try:
        tree, _, _ = diagram.accept(self._scanner.get_next_token(), self._scanner)
        # except ParseException as parse_error:
        #     print(parse_error)
        self.close()
        return tree

    def close(self):
        self._scanner.close()
