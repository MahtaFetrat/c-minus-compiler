from anytree import Node, RenderTree


class Tree:
    def __init__(self, root_name, subtrees):
        self.root_name = root_name
        self.subtrees = subtrees or []

    def __str__(self):
        string = ""
        for pre, _, node in RenderTree(self._get_anytree()):
            string += "%s%s\n" % (pre, node.name)
        return string[:-1]

    def _get_anytree(self, parent=None):
        root = Node(self.root_name, parent)
        for subtree in self.subtrees:
            subtree._get_anytree(root)
        return root
