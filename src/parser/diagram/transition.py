from src.base import Edge, List
from src.parser.diagram.symbol import create_symbol


class Transition(Edge):
    def __init__(self, dest, name, predicts: List[str], symbol_type, diagram=None):
        self.symbol = create_symbol(name, symbol_type, predicts, diagram)
        super().__init__([self.symbol], dest)

    def accept(self, lookahead, scanner):
        return self.symbol.accept(lookahead, scanner), self.dest

    def is_valid(self, character: str):
        return self.symbol.handle(character)
