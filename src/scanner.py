class Scanner:

    def __init__(self):
        self._line_num = 0
        self._character_num = 0

    @property
    def line_num(self):
        return self._line_num

    @line_num.setter
    def line_num(self, num: int):
        self._line_num = num

    @property
    def character_num(self):
        return self._character_num

    @character_num.setter
    def character_num(self, num):
        self._character_num = num

    def get_next_token(self):
        pass
