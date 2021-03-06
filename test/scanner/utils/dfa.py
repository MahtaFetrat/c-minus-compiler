from src.scanner.utils import TokenType


SIMPLE_DFA_DICT = {
    'alphabet': ['1', '9'],
    'states': [
        {
            'id': 0,
            'start': True
        },
        {
            'id': 1,
            'end': True,
            'token_type': TokenType.NUM,
        },
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': ['9']},
        {'id': 1, 'state_src_id': 0, 'state_dst_id': 0, 'symbols': ['1']},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': ['9', '1']},
    ],
}

KEYID_DFA_DICT = {
    'alphabet': ['a', 'b', 'c', '1', '2', '3', ' ', '\n', '='],
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
            'token_type': TokenType.KEYID,
            'roll_back': True
        },
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': ['a', 'b', 'c']},
        {'id': 1, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': ['a', 'b', 'c', '1', '2', '3']},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 2, 'symbols': [' ', '\n', '=']},
    ],
}
