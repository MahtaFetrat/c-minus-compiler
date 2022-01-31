from enum import Enum


class OPCode(Enum):
    EMPTY = ""
    ADD = "ADD"
    MULT = "MULT"
    SUB = "SUB"
    EQUAL = "EQ"
    LESS = "LT"
    ASSIGN = "ASSIGN"
    JUMP_IF = "JPF"
    JUMP = "JP"
    PRINT = "PRINT"


class Assembler:
    _CODE_FORMAT = "%s\t(%s, %s, %s, %s)"

    def __init__(self, data_address, temp_address, stack_address):
        self.data_address = data_address
        self.temp_address = temp_address
        self.stack_address = stack_address
        self.data_pointer = self.data_address
        self.temp_pointer = self.temp_address
        self.program_block = []

    def move_data_pointer(self, delta):
        self.data_address += delta

    def move_temp_pointer(self, delta):
        self.temp_address += delta

    def add_instruction(self, index, opcode, arg1="", arg2="", arg3=""):
        code = self._CODE_FORMAT % (index, opcode.value, arg1, arg2, arg3)
        if index == len(self.program_block):
            self.program_block.append(code)
        else:
            self.program_block[index] = code

    @property
    def code(self):
        return "\n".join(self.program_block)
