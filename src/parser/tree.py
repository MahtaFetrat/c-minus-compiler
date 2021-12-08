from anytree import Node


class Tree:
    def __init__(self, root_name, subtrees):
        self.root_name = root_name
        self.subtrees = subtrees or []

    def get_printable_tree(self, parent=None):
        root = Node(self.root_name, parent=parent)
        print(root)
        for subtree in self.subtrees:
            subtree.get_printable_tree(root)
        return root

    def print(self):
        print(self.root_name)
