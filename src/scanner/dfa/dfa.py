from src.scanner.utils.exceptions import TransferException, RoleBackException


class DFA(object):

    def __init__(self, start_state):
        self._start_state = start_state

    def accepts(self, string) -> bool:
        try:
            state = self._start_state
            for character in string:
                state = state.transfer(character)
            return state.is_final()
        except TransferException:
            return False

    @property
    def start_state(self):
        return self._start_state

