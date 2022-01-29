from typing import Union, Tuple

from src.scanner.utils import Language


class IDItem:
    def __init__(
            self, lookahead=None, scope=None, element_type=None, cell_no=0
    ):
        self.lookahead = lookahead
        self.scope = scope
        self.element_type = element_type
        self.cell_no = cell_no

    def __str__(self):
        return f'{self.lookahead}:{self.scope.get_address(self.lookahead)}'


class Scope:
    def __init__(self, number, parent=None, args_count=0, name=None):
        self.number = number
        self.id_items = []
        self.parent = parent
        self.args_count = args_count
        self.name = name

    @property
    def last_item(self):
        return self.id_items[-1]

    def insert(self, lookahead) -> IDItem:
        item = IDItem(lookahead, self, None)
        self.id_items.append(item)
        return item

    def get_item(self, lookahead) -> Union[IDItem, None]:
        for item in self.id_items:
            if item.lookahead == lookahead:
                return item
        if self.parent:
            return self.parent.get_item(lookahead)
        return None

    def get_address(self, lookahead) -> Union[Tuple[int, int], None]:
        for index, item in enumerate(self.id_items):
            if item.lookahead == lookahead:
                return self.number, index
        if self.parent:
            return self.parent.get_address(lookahead)
        return None

    def __str__(self):
        return ' '.join(map(str, self.id_items))


class SymbolTable:
    keyword = list(set(Language.KEYWORDS.value()))

    def __init__(self):
        self.stack = [Scope(0)]

    @property
    def current_scope(self) -> Scope:
        return self.stack[-1]

    def add_scope(self, lookahead):
        self.stack.append(Scope(
            number=len(self.stack),
            parent=self.current_scope,
            name=lookahead
        ))

    def pop(self):
        return self.stack.pop()

    def add_symbol(self, lookahead):
        token_type = lookahead[0]
        if token_type not in self.keyword:
            self.current_scope.insert(lookahead)
