from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.diagram_dict import DiagramDict
from src.parser.utils import ParseException, MissingException
from src.scanner.scanner import Scanner
from anytree import RenderTree


class Parser:
    START_STATE = "Program"
    PARSE_TREE_FILENAME = "parse_tree.txt"
    SYNTAX_ERROR_FILENAME = "syntax_errors.txt"

    def __init__(self, input_filename):
        self._scanner = Scanner(input_filename)
        self._transition_diagram = Builder(
            DiagramDict().get_transition_diagram_dict()
        ).build_transition_diagram()

    def parse(self):
        diagram = self._transition_diagram[Parser.START_STATE]
        tree, _, _ = diagram.accept(self._scanner.get_next_token(), self._scanner)
        Parser._output_results(tree)
        self.close()

    @staticmethod
    def _output_results(tree):
        Parser._write_parse_tree(tree)
        Parser._write_errors()

    @staticmethod
    def _write_parse_tree(tree):
        with open(Parser.PARSE_TREE_FILENAME, "w") as file:
            file.write(str(tree))

    @staticmethod
    def _write_errors():
        with open(Parser.SYNTAX_ERROR_FILENAME, "w") as file:
            file.write("There is no syntax error.")  # TODO

    def close(self):
        self._scanner.close()
