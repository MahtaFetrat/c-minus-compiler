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
    INVALID_INPUT = 'Invalid Input'
    INVALID_NUMBER = 'Invalid Number'
    UNMATCHED_COMMENT = 'Unmatched Comment'
    UNCLOSED_COMMENT = 'Unclosed Comment'


class Language(Enum):
    DIGITS = '0123456789'
    SYMBOLS = ';:,[](){}+-*=<'
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    WHITESPACES = [' ', '', '\n', '\r', '\t', '\v', '\f', 'EOF']
    STAR = '*'
    EQUAL = '='
    SLASH = '/'
    EOF_COMMENT = ['EOF', '\n']
    KEYWORDS = ["if", "else", "void", "int", "repeat", "break", "until", "return"]

    def value(self):
        return list(super(Language, self).value)

    @classmethod
    def get_all_characters(cls):
        return Language.DIGITS.value() + \
               Language.SYMBOLS.value() + \
               Language.LETTERS.value() + \
               Language.WHITESPACES.value()
