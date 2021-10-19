from src.scanner.dfa import State, Transition
from src.scanner.dfa.dfa import DFA


class Builder(object):

    def __init__(self, dfa_dict):
        self._dfa_dict = dfa_dict

    def build_dfa(self) -> DFA:
        start_state, states = self._build_states()
        self._build_transitions(states)
        return DFA(start_state)

    def _build_states(self):
        start_state = None
        states = {}
        for state in self._dfa_dict['states']:
            new_state = State(
                state_id=state['id'],
                token_type=state.get('token_type'),
                error_type=state.get('error_type'),
                role_back=state.get('role_back')
            )
            states[state['id']] = new_state
            if state.get('start'):
                start_state = new_state

        return start_state, states

    def _build_transitions(self, states):
        for transition in self._dfa_dict['transitions']:
            new_transition = Transition(
                transition['symbols'], states[transition['state_dst_id']]
            )
            states[transition['state_src_id']].add_transition(new_transition)
