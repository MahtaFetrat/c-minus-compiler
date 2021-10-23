from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator import BaseCreator


class STARCreator(BaseCreator):

    @property
    def states(self):
        return [
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
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 6,
                'symbols': STAR
            },
            {
                'state_src_id': 6,
                'state_dst_id': 7,
                'symbols': SLASH
            },
            {
                'state_src_id': 6,
                'state_dst_id': 8,
                'symbols': self.diff(ALL, SLASH)
            },
        ]
