from .base import *
from ...utils import *


class EQUALDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
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
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
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
