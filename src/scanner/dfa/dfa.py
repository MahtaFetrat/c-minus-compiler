from src.scanner.dfa.state import State


class DFA:

    def __init__(self, start_state):
        self._start_state = start_state
        self._terminal_state = None

    def iterate(self, string) -> State:
        """for DFA test"""
        state = self._start_state
        for character in string:
            print(f'chr = {character}')
            print(f'state = {state.__dict__}')
            [print(f'tr = {tr}') for tr in state.transitions]
            state = state.transfer(character)
        self._terminal_state = state
        return state

    @property
    def start_state(self):
        return self._start_state

    @property
    def terminal_state(self):
        return self._terminal_state
