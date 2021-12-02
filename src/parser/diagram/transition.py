from src.base import Edge, List
from src.parser.diagram.state import State
from src.parser.diagram.symbol import create_symbol
from src.parser.utils import SymbolType


class Transition(Edge):

    def __init__(self, dest: 'State',
                 name,
                 predicts: List[str],
                 symbol_type: SymbolType):
        self.symbol = create_symbol(name, symbol_type, predicts)
        super().__init__([self.symbol], dest)

    def is_valid(self, character: str):
        return self.symbol.handle(character)
