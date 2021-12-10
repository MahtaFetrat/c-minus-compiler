from src.parser.diagram import State
from src.parser.tree import Tree
from src.parser.utils import UnexpectedEOFException, IllegalException, ParseException


class Diagram:
    def __init__(self, name: str, start_state: State, final_state: State):
        self.name = name
        self.start_state = start_state
        self.final_state = final_state

    def accept(self, lookahead, scanner, parser):
        subtrees = []
        state = self.start_state
        while not parser.stopped and state is not self.final_state:
            try:
                tree, lookahead, state = state.transfer(lookahead, scanner, parser)
                if tree:
                    subtrees.append(tree)
            except (IllegalException, UnexpectedEOFException) as exc:
                parser.write_error(str(exc))
                if isinstance(exc, IllegalException):
                    lookahead = scanner.get_next_token()
                continue
        return Tree(self.name, subtrees), lookahead, state

    def __str__(self):
        return self.name
