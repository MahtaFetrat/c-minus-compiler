"""Custom exception for state transfer"""


class TransferException(Exception):

    def __init__(self, state_id: int = None):
        self.state_id = state_id
        super().__init__()

    def __str__(self):
        return 'Transfer Error occurred in state %d' % self.state_id

    def __eq__(self, other):
        return self.state_id == other.state_id
