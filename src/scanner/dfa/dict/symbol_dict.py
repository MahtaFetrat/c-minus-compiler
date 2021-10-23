from src.scanner.dfa.dict.base import *
from src.scanner.utils import *


class SYMBOLDFADict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': 9,
                'end': True,
                'token_type': TokenType.SYMBOL
            }
        ]

    @property
    def transitions(self) -> List[Dict[str, Any]]:
        return [
            {
                'state_src_id': 0,
                'state_dst_id': 9,
                'symbols': diff(SYMBOLS, STAR + EQUAL)
            },
        ]
