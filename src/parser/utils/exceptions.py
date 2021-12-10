class ParseException(Exception):
    def __init__(self, state, lookahead, transition=None):
        super().__init__()
        self._state = state
        self._transition = transition
        self._lookahead = lookahead

    def __str__(self):
        raise NotImplementedError

    @property
    def state(self):
        return self._state

    @property
    def transition(self):
        return self._transition


class MissingException(ParseException):
    def __str__(self):
        return f"missing {self._transition.name}"


class IllegalException(ParseException):
    def __str__(self):
        token_type, token_str = self._lookahead
        terminal_title = token_type if token_type in ["ID", "NUM"] else token_str
        return f"illegal {terminal_title}"

    @property
    def transition(self):
        raise ValueError


class UnexpectedEOFException(ParseException):
    def __str__(self):
        return "Unexpected EOF"

    @property
    def transition(self):
        raise ValueError
