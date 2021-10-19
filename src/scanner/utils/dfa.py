from src.scanner.utils import TokenType, Language, ErrorType

_STAR = Language.STAR.value()
_EQUAL = Language.EQUAL.value()
_SLASH = Language.SLASH.value()
_DIGITS = Language.DIGITS.value()
_SYMBOLS = Language.SYMBOLS.value()
_LETTERS = Language.LETTERS.value()
_WHITESPACES = Language.WHITESPACES.value()
_EOF_COMMENT = Language.EOF_COMMENT.value()
_ALL = Language.get_all_characters()


def diff(first, second):
    return list(set(first).difference(set(second)))


DFA_DICT = {
    'alphabet': _ALL,
    'states': [
        {
            'id': 0,
            'start': True
        },
        {
            'id': 1
        },
        {
            'id': 2,
            'end': True,
            'token_type': TokenType.NUM,
            'roll_back': True
        },
        {
            'id': 3,
            'error': True,
            'error_type': ErrorType.INVALID_NUMBER
        },
        {
            'id': 4
        },
        {
            'id': 5,
            'end': True,
            'token_type': TokenType.KEYID,
            'roll_back': True
        },
        {
            'id': 6
        },
        {
            'id': 7,
            'error': True,
            'error_type': ErrorType.UNMATCHED_COMMENT
        },
        {
            'id': 8,
            'end': True,
            'token_type': TokenType.SYMBOL,
            'roll_back': True
        },
        {
            'id': 9
        },
        {
            'id': 10,
            'end': True,
            'token_type': TokenType.SYMBOL,
            'roll_back': True
        },
        {
            'id': 11
        },
        {
            'id': 12,
            'end': True,
            'token_type': TokenType.SYMBOL
        },
        {
            'id': 13,
            'end': True,
            'token_type': TokenType.SYMBOL,
            'roll_back': True
        },
        {
            'id': 14
        },
        {
            'id': 15
        },
        {
            'id': 16
        },
        {
            'id': 17,
            'end': True,
            'token_type': TokenType.COMMENT
        },
        {
            'id': 18
        },
        {
            'id': 19,
            'end': True,
            'token_type': TokenType.COMMENT,
            'roll_back': True
        },
        {
            'id': 20,
            'end': True,
            'token_type': TokenType.WHITESPACE
        },
        {
            'id': 21,
            'error_type': ErrorType.UNCLOSED_COMMENT
        }
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': _DIGITS},
        {'id': 1, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': _DIGITS},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 2, 'symbols': _SYMBOLS + _WHITESPACES},
        {'id': 3, 'state_src_id': 1, 'state_dst_id': 3, 'symbols': _LETTERS},
        {'id': 4, 'state_src_id': 0, 'state_dst_id': 4, 'symbols': _LETTERS},
        {'id': 5, 'state_src_id': 4, 'state_dst_id': 4, 'symbols': _LETTERS + _DIGITS},
        {'id': 6, 'state_src_id': 4, 'state_dst_id': 5, 'symbols': _SYMBOLS + _WHITESPACES},
        {'id': 7, 'state_src_id': 0, 'state_dst_id': 6, 'symbols': _STAR},
        {'id': 8, 'state_src_id': 6, 'state_dst_id': 7, 'symbols': _SLASH},
        {'id': 9, 'state_src_id': 6, 'state_dst_id': 8, 'symbols': _ALL},
        {'id': 10, 'state_src_id': 0, 'state_dst_id': 9, 'symbols': diff(_ALL, _STAR + _EQUAL)},
        {'id': 11, 'state_src_id': 9, 'state_dst_id': 10, 'symbols': _ALL},
        {'id': 12, 'state_src_id': 0, 'state_dst_id': 11, 'symbols': _EQUAL},
        {'id': 13, 'state_src_id': 11, 'state_dst_id': 12, 'symbols': _EQUAL},
        {'id': 14, 'state_src_id': 11, 'state_dst_id': 13, 'symbols': _ALL},
        {'id': 15, 'state_src_id': 0, 'state_dst_id': 14, 'symbols': _SLASH},
        {'id': 16, 'state_src_id': 14, 'state_dst_id': 15, 'symbols': _STAR},
        {'id': 17, 'state_src_id': 15, 'state_dst_id': 15, 'symbols': diff(_ALL, _STAR + _EOF_COMMENT)},
        {'id': 18, 'state_src_id': 15, 'state_dst_id': 16, 'symbols': _STAR},
        {'id': 19, 'state_src_id': 16, 'state_dst_id': 16, 'symbols': _STAR},
        {'id': 20, 'state_src_id': 16, 'state_dst_id': 17, 'symbols': _SLASH},
        {'id': 21, 'state_src_id': 16, 'state_dst_id': 15, 'symbols': diff(_ALL, _STAR + _SLASH)},
        {'id': 22, 'state_src_id': 14, 'state_dst_id': 18, 'symbols': _SLASH},
        {'id': 23, 'state_src_id': 18, 'state_dst_id': 18, 'symbols': diff(_ALL, _EOF_COMMENT)},
        {'id': 24, 'state_src_id': 18, 'state_dst_id': 19, 'symbols': _EOF_COMMENT},
        {'id': 25, 'state_src_id': 0, 'state_dst_id': 20, 'symbols': _WHITESPACES},
        {'id': 26, 'state_src_id': 15, 'state_dst_id': 21, 'symbols': _EOF_COMMENT},
    ],
}
