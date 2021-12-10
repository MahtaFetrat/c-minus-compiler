from src.base import Edge, List
from src.parser.diagram.symbol import create_symbol
from src.parser.utils import SymbolType


class Transition(Edge):
    def __init__(
        self,
        dest,
        name,
        predicts: List[str],
        follows: List[str],
        symbol_type: SymbolType,
        diagram=None,
    ):
        self.symbol = create_symbol(name, symbol_type, predicts, follows, diagram)
        super().__init__([self.symbol], dest)

    @property
    def name(self):
        return self.symbol.name

    def accept(self, lookahead, scanner, parser):
        return self.symbol.accept(lookahead, scanner, parser)

    def is_valid(self, lookahead):
        return self.symbol.is_valid(lookahead)

    def is_missing(self, lookahead):
        return self.symbol.is_missing(lookahead)

    def __str__(self):
        return str(self.symbol)
