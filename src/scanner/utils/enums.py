from enum import Enum


class StateActionType(Enum):
    REGULAR = 0
    ROLE_BACK = 1
    TRANSFER_EXP = 2
    UNFINISHED_EXP = 3


class TokenType(Enum):
    NONE = 0
    NUM = 1
    SYMBOL = 2
    COMMENT = 3
    WHITESPACE = 4
    KEYID = 5


class ErrorType(Enum):
    NONE = ''
    INVALID_INPUT = 'Invalid Input'
    INVALID_NUMBER = 'Invalid Number'
    UNMATCHED_COMMENT = 'Unmatched Comment'
    UNCLOSED_COMMENT = 'Unclosed Comment'
