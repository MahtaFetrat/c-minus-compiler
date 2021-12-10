from typing import List, Tuple, Union

from src.base import Node, EOF
from src.parser.diagram.symbol import Terminal
from src.parser.diagram.transition import Transition
from src.parser.utils import IllegalException, MissingException, UnexpectedEOFException


class State(Node):
    def __init__(
        self, identifier: int, final: bool = False, transitions: List[Transition] = None
    ):
        self.final = final
        super(State, self).__init__(identifier, transitions)

    def check_missing(self, lookahead) -> Tuple[bool, Union[Transition, None]]:
        missing = list(filter(lambda tr: tr.is_missing(lookahead), self._edges))
        if any(missing):
            return True, missing[0]
        terminals = list(
            filter(lambda tr: isinstance(tr.symbol, Terminal), self._edges)
        )
        if any(terminals):
            return True, terminals[0]
        return False, None

    def get_valid_transition(self, lookahead) -> Transition:
        try:
            transition = list(filter(lambda x: x.is_valid(lookahead), self._edges))[0]
            return transition
        except IndexError:
            is_missed, transition = self.check_missing(lookahead)
            exception_cls = (
                MissingException
                if is_missed
                else IllegalException
                if lookahead[1] != EOF
                else UnexpectedEOFException
            )
            exc = exception_cls(state=self, lookahead=lookahead, transition=transition)
            raise exc

    def transfer(self, lookahead, scanner=None, parser=None):
        """:raises IllegalException and UnexpectedEOFException."""
        if scanner is None or parser is None:
            raise ValueError

        try:
            transition = self.get_valid_transition(lookahead)
            tree, lookahead = transition.accept(lookahead, scanner, parser)
            return tree, lookahead, transition.dest
        except MissingException as exc:
            parser.write_error(str(exc))
            return None, lookahead, exc.transition.dest

    def is_final(self) -> bool:
        return self.final

    @property
    def transition(self):
        return self._edges[0]
