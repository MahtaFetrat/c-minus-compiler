from abc import abstractmethod, ABC
from typing import Dict, Any, List


class BaseDFADict(ABC, dict):

    def __init__(self):
        super().__init__({
            K: self.__getattribute__(K) for K in self.keys()
        })

    def keys(self):
        return ['states', 'transitions']

    def items(self):
        return [(K, self.__getattribute__(K)) for K in self.keys()]

    @property
    @abstractmethod
    def states(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def transitions(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
