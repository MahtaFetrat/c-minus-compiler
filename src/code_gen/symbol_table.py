from enum import Enum
from typing import Union, Tuple

from src.scanner.utils import Language


class IDItem:
    class IDVar(Enum):
        VARIABLE = "var"
        ARRAY = "arr"
        FUNCTION = "func"

    class IDType(Enum):
        INT = "int"
        VOID = "void"

    def __init__(
            self, _id=None, scope=None, element_type=None, var=None, cell_no=0
    ):
        self.id = _id
        self.scope = scope
        self.element_type = element_type
        self.var = var
        self.cell_no = cell_no

    def __str__(self):
        return f'{self.id}:{self.scope.get_address(self.id)}'


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
            if item.id == lookahead:
                return item
        if self.parent:
            return self.parent.get_item(lookahead)
        return None

    def get_address(self, lookahead) -> Union[Tuple[int, int], None]:
        for index, item in enumerate(self.id_items):
            if item.id == lookahead:
                return self.number, index
        if self.parent:
            return self.parent.get_address(lookahead)
        return None

    def __str__(self):
        return ' '.join(map(str, self.id_items))

    def add_symbol(self):
        self.id_items.append(IDItem())

    def set_id(self, _id):
        self.id_items[-1].id = _id

    def set_type(self, _type):
        self.id_items[-1].element_type = IDItem.IDType(_type)

    def set_var(self, var):
        self.id_items[-1].var = var

    def set_cell_no(self, cell_no):
        self.id_items[-1].cell_no = cell_no

    def increment_arg_count(self):
        self.args_count += 1


class SymbolTable:
    keyword = list(set(Language.KEYWORDS.value()))

    def __init__(self):
        self.stack = [Scope(0)]

    @property
    def current_scope(self) -> Scope:
        return self.stack[-1]

    def add_scope(self):
        self.stack.append(Scope(
            number=len(self.stack),
            parent=self.current_scope,
            name=self.current_scope.last_item.id
        ))

    def pop(self):
        return self.stack.pop()

    def add_symbol(self):
        self.current_scope.add_symbol()

    def set_id(self, _id):
        self.current_scope.set_id(_id)

    def set_type(self, _type):
        self.current_scope.set_type(_type)

    def set_var(self, var):
        self.current_scope.set_var(var)

    def set_cell_no(self, cell_no):
        self.current_scope.set_cell_no(cell_no)

    def increment_arg_count(self):
        self.current_scope.increment_arg_count()
