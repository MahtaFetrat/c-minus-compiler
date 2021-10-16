from enum import Enum


class StateActionType(Enum):
    REGULAR = 0
    ROLE_BACK = 1
    TRANSFER_EXP = 2
    UNFINISHED_EXP = 3


class TokenType(Enum):
    NONE = 0
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6
    KEYID = 7
