from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator.base import BaseCreator


class WHITESPACECreator(BaseCreator):

    @property
    def states(self):
        return [
            {
                'id': 22,
                'end': True,
                'token_type': TokenType.WHITESPACE
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 22,
                'symbols': WHITESPACES
            }
        ]
