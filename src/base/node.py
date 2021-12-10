from abc import ABC
from typing import List

from src.base.edge import Edge


class Node(ABC):

    def __init__(self,
                 identifier: int,
                 edges: List[Edge] = None):
        self.identifier = identifier
        self._edges = edges or []

    def __eq__(self, other):
        return bool(self.identifier == other.identifier)

    def __str__(self):
        return str(self.identifier)

    def transfer(self, character: str):
        raise NotImplementedError

    def add_transition(self, transition: Edge):
        self._edges.append(transition)
