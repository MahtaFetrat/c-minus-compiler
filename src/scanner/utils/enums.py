from enum import Enum


class TokenType(Enum):
    NONE = 0
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6
