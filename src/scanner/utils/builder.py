from scanner.scanner import State


class Builder(object):

    def __init__(self, dfa: str):
        self._dfa = dfa

    def build(self) -> State:  # return initial state
        pass
