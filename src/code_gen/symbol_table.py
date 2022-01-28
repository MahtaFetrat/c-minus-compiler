from src.scanner.utils import Language


class IDItem:
    def __init__(
            self, lookahead=None, element_type=None, no_args=None, scope=None, address=None
    ):
        self.lookahead = lookahead
        self.element_type = element_type
        self.no_args = no_args
        self.scope = scope
        self.address = address

    def __str__(self):
        return f'{self.lookahead}:{self.address}'


class Scope:
    def __init__(self, parent=None):
        self.stack = []
        self.parent = parent

    def append(self, lookahead):
        item = self.get_item(lookahead)
        if item:
            return item
        else:
            item = IDItem(lookahead, None, None, self, None)
            self.stack.append(item)
            return item

    def get_item(self, lookahead):
        for item in self.stack:
            if item.token == lookahead:
                return item
        if self.parent:
            return self.parent.get_item(lookahead)
        return None

    def __str__(self):
        return ' '.join(map(str, self.stack))


class SymbolTable:
    keyword = list(set(Language.KEYWORDS.value()))

    def __init__(self):
        self.stack = [Scope()]

    @property
    def current_scope(self):
        return self.stack[-1]

    def add_symbol(self, lookahead):
        token_type = lookahead[0]
        if token_type in self.keyword:
            return lookahead
        self.current_scope.append(lookahead)
        return lookahead
