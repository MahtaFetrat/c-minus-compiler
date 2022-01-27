from enum import Enum


class SymbolType(Enum):
    TERMINAL = 0
    NON_TERMINAL = 1
    EPSILON = 2
    SEMANTIC_ACTION = 3
