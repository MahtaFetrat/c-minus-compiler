from src.parser.diagram import State
from src.parser.tree import Tree
from src.parser.utils import ParseException


class Diagram:
    def __init__(self, name: str, start_state: State, final_state: State):
        self.name = name
        self.start_state = start_state
        self.final_state = final_state

    def accept(self, lookahead, scanner, parser):  # TODO: handle error
        subtrees = []
        state = self.start_state
        while state is not self.final_state:
            try:
                tree, lookahead, state = state.transfer(lookahead, scanner, parser)
            except ParseException as e:
                parser.write_error(str(e))
            subtrees.append(tree)
        return Tree(self.name, subtrees), lookahead, state

    @property
    def tree(self):
        return list(map(lambda node: node.name, self._subtrees))

    def __str__(self):
        return self.name
