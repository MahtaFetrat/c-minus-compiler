from .base import *
from ...utils import *


class InitialDict(BaseDFADict):

    @property
    def states(self) -> List[Dict[str, Any]]:
        return [
            {
                'start': True,
                'id': 0
            }
        ]

    @property
    def transitions(self) -> List[Dict[str, Any]]:
        return []
