class ParseException(Exception):
    def __init__(
            self, state, lookahead, transition
    ):
        super().__init__()
        self._state = state
        self._transition = transition
        self.lookahead = lookahead

    def __str__(self):
        return f'{self.args[0]}, state: {self.state}, lookahead: {self.lookahead}'

    @property
    def state(self):
        return self._state

    @property
    def transition(self):
        return self.transition


class MissingException(ParseException):
    pass


class IllegalException(ParseException):

    @property
    def transition(self):
        raise ValueError
