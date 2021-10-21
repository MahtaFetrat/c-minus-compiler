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


class Language(Enum):
    DIGITS = '0123456789'
    SYMBOLS = ';:,[](){}+-*=<'
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    WHITESPACES = [' ', '\n', '\r', '\t', '\v', '\f', '']
    STAR = '*'
    EQUAL = '='
    SLASH = '/'
    EOF = '\0'
    EOF_COMMENT = ['\0', '\n']
    KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']

    def value(self):
        return list(super(Language, self).value)

    @classmethod
    def get_all_characters(cls):
        return Language.DIGITS.value() + \
               Language.SYMBOLS.value() + \
               Language.LETTERS.value() + \
               Language.WHITESPACES.value() + \
               Language.SLASH.value() + \
               Language.EOF.value()
