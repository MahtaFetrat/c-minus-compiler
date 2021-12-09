from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.diagram_dict import DiagramDict
from src.scanner.scanner import Scanner


class Parser:
    START_STATE = "Program"
    PARSE_TREE_FILENAME = "parse_tree.txt"
    SYNTAX_ERROR_FILENAME = "syntax_errors.txt"

    def __init__(self, input_filename):
        self._scanner = Scanner(input_filename)
        self._transition_diagram = Builder(
            DiagramDict().get_transition_diagram_dict()
        ).build_transition_diagram()

        self._syntax_error_encountered = False
        self._error_out_file = open(Parser.SYNTAX_ERROR_FILENAME, "w")

    def parse(self):
        diagram = self._transition_diagram[Parser.START_STATE]
        tree, _, _ = diagram.accept(self._scanner.get_next_token(), self._scanner, self)
        Parser._write_parse_tree(tree)
        self.close()

    @staticmethod
    def _write_parse_tree(tree):
        with open(Parser.PARSE_TREE_FILENAME, "w") as file:
            file.write(str(tree))

    def write_error(self, error_msg):
        self._syntax_error_encountered = True
        self._error_out_file.write(
            f"#{self._scanner.line_num} : syntax error, {error_msg}\n"
        )

    def close(self):
        self._scanner.close()
        if not self._syntax_error_encountered:
            self._error_out_file.write("There is no syntax error.")
        self._error_out_file.close()
