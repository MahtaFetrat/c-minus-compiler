from src.parser.diagram.builder import Builder
from src.parser.diagram.dict.dict import TRANSITION_DIAGRAM


class Parser:

    def __init__(self):
        self._diagrams = Builder(TRANSITION_DIAGRAM).build_transition_diagrams()

    @classmethod
    def get_diagram_by_name(cls, name):
        pass
