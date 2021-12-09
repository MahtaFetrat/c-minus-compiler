from src.parser.diagram import State
from src.parser.tree import Tree


class Diagram:
    def __init__(self, name: str, start_node: State):
        self.name = name
        self.start_node = start_node
        self._subtrees = []

    def accept(self, lookahead, scanner):  # TODO: handle error
        state = self.start_node
        while not state.is_final():
            tree, lookahead, state = state.transfer(lookahead, scanner)
            self._subtrees.append(tree)
        return Tree(self.name, self._subtrees), lookahead, state

    @property
    def tree(self):
        return list(map(lambda node: node.name, self._subtrees))

    def __str__(self):
        return self.name
