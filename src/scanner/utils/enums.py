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


class Language(Enum):
    DIGITS = '0123456789'
    SYMBOLS = ';:,[](){}+-*=<'
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    WHITESPACES = [' ', '', '\n', '\r', '\t', '\v', '\f', 'EOF']
    STAR = '*'
    EQUAL = '='
    SLASH = '\\'
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
