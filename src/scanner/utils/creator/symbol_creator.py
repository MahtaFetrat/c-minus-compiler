from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator.base import BaseCreator


class SYMBOLCreator(BaseCreator):

    @property
    def states(self):
        return [
            {
                'id': 9,
                'end': True,
                'token_type': TokenType.SYMBOL
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 9,
                'symbols': self.diff(SYMBOLS, STAR + EQUAL)
            },
        ]
