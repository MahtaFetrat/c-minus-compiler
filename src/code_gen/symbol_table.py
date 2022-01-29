from typing import Union

from src.scanner.utils import Language


class IDItem:
    def __init__(
            self, lookahead=None, scope=None, element_type=None, no_args=None
    ):
        self.lookahead = lookahead
        self.scope = scope
        self.element_type = element_type
        self.no_args = no_args

    @property
    def index(self):
        return self.scope.get_address(self)

    def __str__(self):
        return f'{self.lookahead}:{self.index}'


class Scope:
    def __init__(self, parent=None):
        self.stack = []
        self.parent = parent

    def insert(self, lookahead) -> IDItem:
        item = IDItem(lookahead, self, None, None)
        self.stack.append(item)
        return item

    def get_item(self, lookahead) -> Union[IDItem, None]:
        for item in self.stack:
            if item.token == lookahead:
                return item
        if self.parent:
            return self.parent.get_item(lookahead)
        return None

    def get_address(self, item):
        try:
            return self.stack.index(item)
        except ValueError:
            return None

    def __str__(self):
        return ' '.join(map(str, self.stack))


class SymbolTable:
    keyword = list(set(Language.KEYWORDS.value()))

    def __init__(self):
        self.stack = [Scope()]

    @property
    def current_scope(self) -> Scope:
        return self.stack[-1]

    def add_scope(self):
        self.stack.append(Scope(self.current_scope))

    def remove_scope(self):
        self.stack.pop()

    def add_symbol(self, lookahead):
        token_type = lookahead[0]
        if token_type not in self.keyword:
            self.current_scope.insert(lookahead)
