from src.parser.tree import Tree


class Diagram:
    def __init__(self, name, start_node):
        self.name = name
        self.start_node = start_node
        self._subtrees = []

    def accept(self, lookahead, scanner):  # TODO: handle error
        state = self.start_node
        while not state.is_final():
            transition = state.transfer(lookahead)
            tree, lookahead, state = transition.accept(lookahead, scanner)
            self._subtrees.append(tree)
        return Tree(self.name, self._subtrees), lookahead

    @property
    def tree(self):
        return list(map(lambda node: node.name, self._subtrees))
