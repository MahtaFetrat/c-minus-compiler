from abc import ABC
from typing import List

from src.parser.utils import SymbolType


class Symbol(ABC):
    def __init__(self, name: str, predicts: List[str]):
        self.name = name
        self.predicts = predicts

    def handle(self, character: str) -> bool:
        raise NotImplementedError


class Terminal(Symbol):

    def handle(self, character: str) -> bool:
        return bool(self.name == character)


class NonTerminal(Symbol):

    def handle(self, character: str) -> bool:
        return bool(character in self.predicts)


class Epsilon(Symbol):

    def handle(self, character: str) -> bool:
        return bool(character in self.predicts)


__ALL = {
    SymbolType.TERMINAL: Terminal,
    SymbolType.NON_TERMINAL: NonTerminal,
    SymbolType.EPSILON: Epsilon
}


def create_symbol(name,
                  symbol_type: SymbolType,
                  predicts: List[str] = None):
    return __ALL[symbol_type](name, predicts)
