from enum import Enum


class StateType(Enum):
    START = 0
    END = 1
    MIDDLE = 2


class TokenType(Enum):
    NONE = 0
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6
