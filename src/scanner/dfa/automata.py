from scanner.scanner import State
from scanner.scanner import TransferException


class Automata(object):

    def __init__(self, initial: State):
        self._initial = initial

    def accepts(self, string) -> bool:
        try:
            state = self._initial
            for character in string:
                state = state.transfer(character)
            return state.is_final()
        except TransferException:
            return False
