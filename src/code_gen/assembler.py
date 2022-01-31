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
    _OUTPUT_FUNCTION_CODE = [
            "0\t(JP, 11,, )",
            "1\t(ASSIGN,  #-1, 508, )",
            "2\t(ADD, 500, 16, 500)",
            "3.\t(ASSIGN, 508, 540, )",
            "4.\t(ADD, 540, 12, 540)",
            "5.\t(ASSIGN, @540, 540, )",
            "6.\t(PRINT, 540)",
            "7\t(SUB, 500, 16, 500)",
            "8\t(ADD, 508, 4, 548)",
            "9\t(ASSIGN, @548, 548, )",
            "10\t(JP, @548, , )"
        ]

    def __init__(self, data_address, temp_address, stack_address):
        self.data_address = data_address
        self.temp_address = temp_address
        self.stack_address = stack_address
        self.data_pointer = self.data_address
        self.temp_pointer = self.temp_address
        self.program_block = self._OUTPUT_FUNCTION_CODE.copy()

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
