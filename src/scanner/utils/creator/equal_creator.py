from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator.base import BaseCreator


class EQUALCreator(BaseCreator):

    @property
    def states(self):
        return [
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
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 11,
                'symbols': EQUAL
            },
            {
                'state_src_id': 11,
                'state_dst_id': 12,
                'symbols': EQUAL
            },
            {
                'state_src_id': 11,
                'state_dst_id': 13,
                'symbols': ALL
            },
        ]
