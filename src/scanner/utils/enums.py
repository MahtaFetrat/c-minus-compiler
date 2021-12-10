import string

from enum import Enum


class TokenType(Enum):
    NONE = 0
    NUM = 1
    SYMBOL = 2
    COMMENT = 3
    WHITESPACE = 4
    KEYID = 5


class ErrorType(Enum):
    NONE = ''
    INVALID_INPUT = 'Invalid input'
    INVALID_NUMBER = 'Invalid number'
    UNMATCHED_COMMENT = 'Unmatched comment'
    UNCLOSED_COMMENT = 'Unclosed comment'


class TransitionType(Enum):
    INCLUDE = 0
    EXCLUDE = 1


class Language(Enum):
    EOF = '\0'
    STAR = '*'
    EQUAL = '='
    SLASH = '/'
    NEW_LINE = '\n'
    DIGITS = string.digits
    LETTERS = string.ascii_letters
    SYMBOLS = ';:,[](){}+-*=<'
    WHITESPACES = [' ', '\n', '\r', '\t', '\v', '\f', '\0']
    KEYWORDS = ['if', 'endif', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']

    def value(self):
        return list(super(Language, self).value)

    @classmethod
    def get_all_characters(cls):
        return Language.SLASH.value() + \
               Language.DIGITS.value() + \
               Language.SYMBOLS.value() + \
               Language.LETTERS.value() + \
               Language.WHITESPACES.value()
