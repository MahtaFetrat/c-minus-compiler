from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator.base import BaseCreator


class KEYIDCreator(BaseCreator):

    @property
    def states(self):
        return [
            {
                'id': 4
            },
            {
                'id': 5,
                'end': True,
                'token_type': TokenType.KEYID,
                'roll_back': True
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 4,
                'symbols': LETTERS
            },
            {
                'state_src_id': 4,
                'state_dst_id': 4,
                'symbols': LETTERS + DIGITS
            },
            {
                'state_src_id': 4,
                'state_dst_id': 5,
                'symbols': SYMBOLS + WHITESPACES
            },
        ]
