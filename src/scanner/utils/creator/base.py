

class BaseCreator:

    INITIAL_STATE_ID = 0

    @property
    def states(self):
        return [
            {
                'start': True,
                'id': self.INITIAL_STATE_ID
            }
        ]

    @property
    def transitions(self):
        if isinstance(self, BaseCreator):
            return []
        raise NotImplementedError

    @staticmethod
    def diff(first, second):
        return list(set(first).difference(set(second)))
