from src.base import Node


class State(Node):
    def __init__(self, identifier: int, final: bool = False, transitions=None):
        self.final = final
        super(State, self).__init__(identifier, transitions)

    def transfer(self, lookahead):  # TODO: panic mode error handling
        transition = list(filter(lambda x: x.is_valid(lookahead), self._edges))[0]
        return transition

    def is_final(self) -> bool:
        return self.final

    @property
    def transition(self):
        return self._edges[0]
