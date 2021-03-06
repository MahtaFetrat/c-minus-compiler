from abc import ABC
from typing import List

from src.parser.utils import SymbolType
from src.parser.tree import Tree


class Symbol(ABC):
    def __init__(
            self, name: str, predicts: List[str], follows: List[str], diagram=None
    ):
        self.name = name
        self.predicts = predicts
        self.follows = follows
        self.diagram = diagram

    def is_valid(self, lookahead, dest=None) -> bool:
        token_type, token_string = lookahead
        return bool(token_type in self.predicts or token_string in self.predicts)

    def accept(self, lookahead, scanner, parser):
        raise NotImplementedError

    def is_missing(self, lookahead) -> bool:
        token_type, token_string = lookahead
        return bool(token_type in self.follows or token_string in self.follows)

    def __str__(self):
        return self.name + " {" + ", ".join(self.predicts) + "}"


class Terminal(Symbol):
    def accept(self, lookahead, scanner, parser):
        return Tree(Terminal.token_repr(lookahead), None), scanner.get_next_token()

    @staticmethod
    def token_repr(lookahead):
        token_type, token_str = lookahead
        return f"({str(token_type)}, {token_str})" if token_str != "$" else "$"


class NonTerminal(Symbol):
    def accept(self, lookahead, scanner, parser):
        tree, lookahead, _ = self.diagram.accept(lookahead, scanner, parser)
        return tree, lookahead


class Epsilon(Symbol):
    def accept(self, lookahead, scanner, parser):
        return Tree("epsilon", None), lookahead


class SemanticAction(Symbol):
    def accept(self, lookahead, scanner, parser):
        return Tree(self.name, None), lookahead

    def is_valid(self, lookahead, dest=None) -> bool:
        if not dest:
            raise ValueError

        transitions = list(filter(lambda x: x.is_valid(lookahead), dest.transitions))
        return True if (transitions or not dest.transitions) else False

    def is_missing(self, lookahead):
        return False


__all__ = {
    SymbolType.TERMINAL: Terminal,
    SymbolType.NON_TERMINAL: NonTerminal,
    SymbolType.EPSILON: Epsilon,
    SymbolType.SEMANTIC_ACTION: SemanticAction
}


def create_symbol(
        name,
        symbol_type: SymbolType,
        predicts: List[str] = None,
        follows: List[str] = None,
        diagram=None,
):
    return __all__[symbol_type](name, predicts, follows, diagram)
