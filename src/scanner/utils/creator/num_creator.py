from src.scanner.utils.creator.__extra__ import *
from src.scanner.utils.creator import BaseCreator


class NUMCreator(BaseCreator):

    @property
    def states(self):
        return [
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
            }
        ]

    @property
    def transitions(self):
        return [
            {
                'state_src_id': self.INITIAL_STATE_ID,
                'state_dst_id': 1,
                'symbols': DIGITS
            },
            {
                'state_src_id': 1,
                'state_dst_id': 1,
                'symbols': DIGITS
            },
            {
                'state_src_id': 1,
                'state_dst_id': 2,
                'symbols': self.diff(ALL, LETTERS + DIGITS)
            },
            {
                'state_src_id': 1,
                'state_dst_id': 3,
                'symbols': self.diff(ALL, LETTERS),
                'type': TransitionType.EXCLUDE
            }
        ]
