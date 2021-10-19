from src.scanner.utils import TokenType


simple_dfa_dict = {
    'alphabet': ['*', '9'],
    'states': [
        {
            'id': 0,
            'end': False,
            'start': True,
            'type': TokenType.NONE,
        },
        {
            'id': 1,
            'end': True,
            'start': False,
            'type': TokenType.NUM,
        },
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': ['9']},
        {'id': 1, 'state_src_id': 0, 'state_dst_id': 0, 'symbols': ['*']},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': ['9', '*']},
    ],
}

key_id_dfa_dict = {
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
            'type': TokenType.KEYID,
            'role_back': True
        },
    ],
    'transitions': [
        {'id': 0, 'state_src_id': 0, 'state_dst_id': 1, 'symbols': ['a', 'b', 'c']},
        {'id': 1, 'state_src_id': 1, 'state_dst_id': 1, 'symbols': ['a', 'b', 'c', '1', '2', '3']},
        {'id': 2, 'state_src_id': 1, 'state_dst_id': 2, 'symbols': [' ', '\n', '=']},
    ],
}

DFA_TABLE = {
    'simple': simple_dfa_dict,
    'keyid': key_id_dfa_dict
}
