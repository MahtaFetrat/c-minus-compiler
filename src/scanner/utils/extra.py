from typing import List

from .enums import *

EOF: List[str] = Language.EOF.value()
STAR: List[str] = Language.STAR.value()
EQUAL: List[str] = Language.EQUAL.value()
SLASH: List[str] = Language.SLASH.value()
DIGITS: List[str] = Language.DIGITS.value()
SYMBOLS: List[str] = Language.SYMBOLS.value()
LETTERS: List[str] = Language.LETTERS.value()
NEW_LINE: List[str] = Language.NEW_LINE.value()
WHITESPACES: List[str] = Language.WHITESPACES.value()

ALL: List[str] = Language.get_all_characters()


def diff(first, second):
    return list(set(first).difference(set(second)))
