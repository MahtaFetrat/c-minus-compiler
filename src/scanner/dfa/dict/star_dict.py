from .base import *
from ...utils import *


class STARDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
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
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
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
                'symbols': diff(ALL, SLASH)
            },
        ]
