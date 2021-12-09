from typing import List, Tuple

from src.base import Node
from src.parser.diagram.transition import Transition
from src.parser.tree import Tree
from src.parser.utils import (
    MissingNTException,
    IllegalException,
    MissingTException,
)


class State(Node):
    def __init__(
        self, identifier: int, final: bool = False, transitions: List[Transition] = None
    ):
        self.final = final
        super(State, self).__init__(identifier, transitions)

    def check_missing(self, lookahead) -> Tuple[bool, Transition]:
        missing = list(filter(lambda tr: tr.is_missing(lookahead), self._edges))
        return (True, missing[0]) if any(missing) else (False, None)

    def get_valid_transition(self, lookahead, parser) -> Transition:
        try:
            transition = list(filter(lambda x: x.is_valid(lookahead), self._edges))[0]
            return transition
        except IndexError:
            is_missed, transition = self.check_missing(lookahead)
            exception_cls = MissingNTException if is_missed else IllegalException
            # TODO: right MisssingException class
            e = exception_cls(state=self, lookahead=lookahead, transition=transition)
            parser.write_error(str(e))
            raise e

    def transfer(self, lookahead, scanner=None, parser=None):
        """:raises IllegalException and UnexpectedEOFException."""
        if scanner is None or parser is None:
            raise ValueError
        try:
            transition = self.get_valid_transition(lookahead, parser)
            tree, lookahead = transition.accept(lookahead, scanner, parser)
            return tree, lookahead, transition.dest
        except (MissingTException, MissingNTException) as e:
            if e.__class__ == MissingNTException.__class__:
                lookahead = scanner.get_next_token()
            return None, lookahead, e.transition.dest

    def is_final(self) -> bool:
        return self.final

    @property
    def transition(self):
        return self._edges[0]
