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

    def is_valid(self, lookahead) -> bool:
        token_type, token_string = lookahead
        return bool(token_type in self.predicts or token_string in self.predicts)

    def accept(self, lookahead, scanner):
        raise NotImplementedError

    def is_missing(self, lookahead):
        token_type, token_string = lookahead
        return bool(token_type in self.follows or token_string in self.follows)

    def __str__(self):
        return self.name + " {" + ", ".join(self.predicts) + "}"


class Terminal(Symbol):
    def accept(self, lookahead, scanner):
        return Tree(str(lookahead), None), scanner.get_next_token()


class NonTerminal(Symbol):
    def accept(self, lookahead, scanner):
        tree, lookahead, _ = self.diagram.accept(lookahead, scanner)
        return tree, lookahead


class Epsilon(Symbol):
    def accept(self, lookahead, scanner):
        return Tree("epsilon", None), lookahead


__all__ = {
    SymbolType.TERMINAL: Terminal,
    SymbolType.NON_TERMINAL: NonTerminal,
    SymbolType.EPSILON: Epsilon,
}


def create_symbol(
        name, symbol_type: SymbolType,
        predicts: List[str] = None, follows: List[str] = None, diagram=None
):
    return __all__[symbol_type](name, predicts, follows, diagram)
