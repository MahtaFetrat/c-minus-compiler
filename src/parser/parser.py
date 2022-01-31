from src.code_gen.code_gen import CodeGen

from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.diagram_dict import DiagramDict
from src.parser.tree import Tree
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
        self._unexpected_eof_encountered = False
        self._error_out_file = open(Parser.SYNTAX_ERROR_FILENAME, "w")

        self.code_gen = CodeGen()

    @property
    def stopped(self):
        return self._unexpected_eof_encountered

    def parse(self):
        diagram = self._transition_diagram[Parser.START_STATE]
        tree, _, _ = diagram.accept(self._scanner.get_next_token(), self._scanner, self)
        self.close()

    @staticmethod
    def _write_parse_tree(tree: Tree):
        with open(Parser.PARSE_TREE_FILENAME, "w", encoding="utf-8") as file:
            file.write(str(tree))

    def write_error(self, error_msg):
        self._syntax_error_encountered = True
        if "Unexpected EOF" in error_msg:
            self._unexpected_eof_encountered = True
        self._error_out_file.write(
            f"#{self._scanner.line_num} : syntax error, {error_msg}\n"
        )

    def close(self):
        self._scanner.close()
        self.code_gen.close()
        if not self._syntax_error_encountered:
            self._error_out_file.write("There is no syntax error.")
        self._error_out_file.close()
