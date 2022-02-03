from enum import Enum


class OPCode(Enum):
    EMPTY = ""
    ADD = "ADD"
    MULT = "MULT"
    SUB = "SUB"
    EQUAL = "EQ"
    LESS = "LT"
    ASSIGN = "ASSIGN"
    JUMP_FALSE = "JPF"
    JUMP = "JP"
    PRINT = "PRINT"


class Assembler:
    _CODE_FORMAT = "%s\t(%s, %s, %s, %s)"

    def __init__(self, data_address, temp_address, stack_address, runtime_stack_top):
        self.data_address = data_address
        self.temp_address = temp_address
        self.stack_address = stack_address
        self.data_pointer = self.data_address
        self.temp_pointer = self.temp_address
        self.program_block = [
            f"0\t(ASSIGN, #{stack_address}, {runtime_stack_top}, )",
            "1\t(ASSIGN, #-1, 508, )",
            "2\t(JP, 14, , )",
            "3\t(ADD, 500, #16, 500)",
            "4\t(ADD, 508, #8, 10000)",
            "5\t(ASSIGN, #0, @10000, )",
            "6\t(ASSIGN, 508, 10004, )",
            "7\t(ADD, 10004, #12, 10004)",
            "8\t(ASSIGN, @10004, 10004, )",
            "9\t(PRINT, 10004)",
            "10\t(SUB, 500, #16, 500)",
            "11\t(ADD, 508, #4, 10008)",
            "12\t(ASSIGN, @10008, 10008, )",
            "13\t(JP, @10008, , )"
        ]

    def move_data_pointer(self, delta):
        self.data_address += delta

    def move_temp_pointer(self, delta):
        self.temp_address += delta

    def add_instruction(self, index, opcode, arg1="", arg2="", arg3=""):
        code = self._CODE_FORMAT % (index, opcode.value, arg1, arg2, arg3)
        print(code)
        if index == len(self.program_block):
            self.program_block.append(code)
        else:
            self.program_block[index] = code

    @property
    def code(self):
        return "\n".join(self.program_block)
