from src.base import Edge, List
from src.parser.diagram.symbol import create_symbol
from src.parser.utils import SymbolType


class Transition(Edge):
    def __init__(
        self, dest, name, predicts: List[str], symbol_type: SymbolType, diagram=None
    ):
        self.symbol = create_symbol(name, symbol_type, predicts, diagram)
        super().__init__([self.symbol], dest)

    def accept(self, lookahead, scanner):
        tree, lookahead = self.symbol.accept(lookahead, scanner)
        return tree, lookahead, self.dest

    def is_valid(self, lookahead):
        return self.symbol.handle(lookahead)

    def __str__(self):
        return str(self.symbol)
