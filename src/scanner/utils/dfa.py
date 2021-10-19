from src.scanner.utils import TokenType, Language

STAR = Language.STAR.value()
EQUAL = Language.EQUAL.value()
SLASH = Language.SLASH.value()
DIGITS = Language.DIGITS.value()
SYMBOLS = Language.SYMBOLS.value()
LETTERS = Language.LETTERS.value()
WHITESPACES = Language.WHITESPACES.value()
EOF_COMMENT = Language.EOF_COMMENT.value()
ALL = Language.get_all_characters()


def diff(first, second):
    return list(set(first).difference(set(second)))


dfa_dict = {
    'alphabet': ALL,
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
            'type': TokenType.NUM,
            'role_back': True
        },
        {
            'id': 3,
            'error': True
        },
        {
            'id': 4
        },
        {
            'id': 5,
            'end': True,
            'type': TokenType.KEYID,
            'role_back': True
        },
        {
            'id': 6
        },
        {
            'id': 7,
            'error': True
        },
        {
            'id': 8,
            'end': True,
            'type': TokenType.SYMBOL,
            'role_back': True
        },
        {
            'id': 9
        },
        {
            'id': 10,
            'end': True,
            'type': TokenType.SYMBOL,
            'role_back': True
        },
        {
            'id': 11
        },
        {
            'id': 12,
            'end': True,
            'type': TokenType.SYMBOL
        },
        {
            'id': 13,
            'end': True,
            'type': TokenType.SYMBOL,
            'role_back': True
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
            'type': TokenType.COMMENT
        },
        {
            'id': 18
        },
        {
            'id': 19,
            'end': True,
            'type': TokenType.COMMENT,
            'role_back': True
        },
        {
            'id': 20,
            'end': True,
            'type': TokenType.WHITESPACE
        }
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': DIGITS},
        {'id': 1, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': DIGITS},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 2, 'symbols': SYMBOLS + WHITESPACES},
        {'id': 3, 'state_src_id': 1, 'state_dst_id': 3, 'symbols': LETTERS},
        {'id': 4, 'state_src_id': 0, 'state_dst_id': 4, 'symbols': LETTERS},
        {'id': 5, 'state_src_id': 4, 'state_dst_id': 4, 'symbols': LETTERS + DIGITS},
        {'id': 6, 'state_src_id': 4, 'state_dst_id': 5, 'symbols': SYMBOLS + WHITESPACES},
        {'id': 7, 'state_src_id': 0, 'state_dst_id': 6, 'symbols': STAR},
        {'id': 8, 'state_src_id': 6, 'state_dst_id': 7, 'symbols': SLASH},
        {'id': 9, 'state_src_id': 6, 'state_dst_id': 8, 'symbols': ALL},
        {'id': 10, 'state_src_id': 0, 'state_dst_id': 9, 'symbols': diff(ALL, STAR + EQUAL)},
        {'id': 11, 'state_src_id': 9, 'state_dst_id': 10, 'symbols': ALL},
        {'id': 12, 'state_src_id': 0, 'state_dst_id': 11, 'symbols': EQUAL},
        {'id': 13, 'state_src_id': 11, 'state_dst_id': 12, 'symbols': EQUAL},
        {'id': 14, 'state_src_id': 11, 'state_dst_id': 13, 'symbols': ALL},
        {'id': 15, 'state_src_id': 0, 'state_dst_id': 14, 'symbols': SLASH},
        {'id': 16, 'state_src_id': 14, 'state_dst_id': 15, 'symbols': STAR},
        {'id': 17, 'state_src_id': 15, 'state_dst_id': 15, 'symbols': diff(ALL, STAR)},
        {'id': 18, 'state_src_id': 15, 'state_dst_id': 16, 'symbols': diff(ALL, STAR)},
        {'id': 19, 'state_src_id': 16, 'state_dst_id': 16, 'symbols': STAR},
        {'id': 20, 'state_src_id': 16, 'state_dst_id': 15, 'symbols': diff(ALL, STAR + SLASH)},
        {'id': 21, 'state_src_id': 17, 'state_dst_id': 18, 'symbols': SLASH},
        {'id': 22, 'state_src_id': 18, 'state_dst_id': 18, 'symbols': diff(ALL, EOF_COMMENT)},
        {'id': 23, 'state_src_id': 18, 'state_dst_id': 19, 'symbols': EOF_COMMENT},
        {'id': 24, 'state_src_id': 0, 'state_dst_id': 20, 'symbols': WHITESPACES}
    ],
}
