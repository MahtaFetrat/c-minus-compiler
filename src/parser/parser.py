from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.dict import TRANSITION_DIAGRAM


class Parser:
    def __init__(self):
        self._transition_diagram = Builder(
            TRANSITION_DIAGRAM
        ).build_transition_diagram()

    @classmethod
    def get_diagram_by_name(cls, name):
        pass
