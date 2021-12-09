from typing import List, Tuple

from src.base import Node
from src.parser.diagram.transition import Transition
from src.parser.utils import MissingException, IllegalException


class State(Node):
    def __init__(
            self, identifier: int, final: bool = False, transitions: List[Transition] = None
    ):
        self.final = final
        super(State, self).__init__(identifier, transitions)

    def check_missing(self, lookahead) -> Tuple[bool, Transition]:
        missing = list(filter(lambda tr: tr.is_missing(lookahead), self._edges))
        return (True, missing[0]) if any(missing) else (False, None)

    def get_valid_transition(self, lookahead) -> Transition:
        try:
            transition = list(filter(lambda x: x.is_valid(lookahead), self._edges))[0]
            return transition
        except IndexError:
            is_missed, transition = self.check_missing(lookahead)
            exception_cls = MissingException if is_missed else IllegalException
            raise exception_cls(
                state=self,
                lookahead=lookahead,
                transition=transition
            )

    def transfer(self, lookahead, scanner=None):
        if scanner is None:
            raise ValueError

        transition = self.get_valid_transition(lookahead)
        tree, lookahead = transition.accept(lookahead, scanner)
        return tree, lookahead, transition.dest

    def is_final(self) -> bool:
        return self.final

    @property
    def transition(self):
        return self._edges[0]
