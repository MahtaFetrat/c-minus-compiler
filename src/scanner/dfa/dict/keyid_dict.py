from .base import *
from ...utils import *


class KEYIDDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
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
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
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
                'symbols': diff(ALL, LETTERS + DIGITS)
            },
        ]
