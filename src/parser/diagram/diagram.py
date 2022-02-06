from src.code_gen.utils.exceptions import SemanticException
from src.parser.diagram import State
from src.parser.tree import Tree
from src.parser.utils import IllegalException, ParseException, MissingException


class Diagram:
    def __init__(self, name: str, start_state: State, final_state: State):
        self.name = name
        self.start_state = start_state
        self.final_state = final_state

    def accept(self, lookahead, scanner, parser):
        subtrees = []
        state = self.start_state
        while not parser.stopped and state is not self.final_state:
            try:
                tree, lookahead, state = state.transfer(lookahead, scanner, parser)
                if tree:
                    subtrees.append(tree)
                    if tree.root_name.startswith("#"):
                        parser.code_gen.call(tree.root_name, lookahead)
            except ParseException as exc:
                parser.write_error(str(exc))
                if isinstance(exc, IllegalException):
                    lookahead = scanner.get_next_token()
                if isinstance(exc, MissingException):
                    state = exc.transition.dest
                continue
            except SemanticException as exc:
                parser.write_semantic_error(str(exc))
            except:
                pass
        return Tree(self.name, subtrees), lookahead, state

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
