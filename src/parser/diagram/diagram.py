class Diagram:

    def __init__(self, start_node):
        self.start_node = start_node
        self._tree = []

    def accept(self, character):  # TODO: handle error
        state = self.start_node
        self._tree = [state.transition]
        while not (state.is_final() or state.is_error()):
            state = state.transfer(character)
            self._tree.append(state.transition)
        return not state.is_error()

    @property
    def tree(self):
        return list(map(lambda node: node.name, self._tree))
