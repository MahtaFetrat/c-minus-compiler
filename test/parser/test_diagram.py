import unittest

from src.parser import DiagramDict, Builder


class TestDiagram(unittest.TestCase):

    def setUp(self) -> None:
        self.diagram_dict = DiagramDict()
        self.tr_diagram_dict = self.diagram_dict.get_transition_diagram_dict()

    def test_get_transition_diagram_dict(self):
        self.assertEqual(len(self.tr_diagram_dict), 45)
        self.assertEqual(self.diagram_dict.state_id, 163)

    def test_diagram_builder(self):
        diagram = Builder(self.tr_diagram_dict).build_transition_diagram()
        self.assertEqual(len(diagram), 45)


if __name__ == '__main__':
    unittest.main()
