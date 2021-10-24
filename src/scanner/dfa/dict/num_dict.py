from .base import *
from ...utils import *


class NUMDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
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
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
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
                'symbols': diff(ALL, LETTERS + DIGITS)
            },
            {
                'state_src_id': 1,
                'state_dst_id': 3,
                'symbols': diff(ALL, LETTERS),
                'type': TransitionType.EXCLUDE
            }
        ]
