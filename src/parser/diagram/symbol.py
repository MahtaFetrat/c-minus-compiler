from abc import ABC
from typing import List

from src.parser.utils import SymbolType
from src.parser.tree import Tree


class Symbol(ABC):
    def __init__(self, name: str, predicts: List[str], diagram=None):
        self.name = name
        self.predicts = predicts
        self.diagram = diagram

    def handle(self, character: str) -> bool:
        return bool(character in self.predicts)

    def accept(self, lookahead, scanner):
        raise NotImplementedError


class Terminal(Symbol):
    def accept(self, lookahead, scanner):
        return Tree(self.name, None), scanner.get_next_token()


class NonTerminal(Symbol):
    def __init__(self, name: str, predicts: List[str]):
        super().__init__(name, predicts)

    def accept(self, lookahead, scanner):
        return self.diagram.accept(lookahead, scanner)


class Epsilon(Symbol):
    def accept(self, lookahead, scanner):
        return None, lookahead


__ALL = {
    SymbolType.TERMINAL: Terminal,
    SymbolType.NON_TERMINAL: NonTerminal,
    SymbolType.EPSILON: Epsilon,
}


def create_symbol(name, symbol_type: SymbolType, predicts: List[str] = None):
    return __ALL[symbol_type](name, predicts)
