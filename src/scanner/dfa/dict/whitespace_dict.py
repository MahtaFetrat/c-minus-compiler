from .base import *
from ...utils import *


class WHITESPACEDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': 22,
                'end': True,
                'token_type': TokenType.WHITESPACE
            }
        ]

    @property
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
                'state_dst_id': 22,
                'symbols': WHITESPACES
            }
        ]
