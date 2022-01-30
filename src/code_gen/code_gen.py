from typing import Dict, Any

from src.code_gen.assembler import Assembler, OPCode
from src.code_gen.symbol_table import SymbolTable, IDItem


class CodeGen:
    _WORD_SIZE = 4
    _DATA_ADDRESS = 100
    _TEMP_ADDRESS = 500
    _RUNTIME_STACK_TOP = _TEMP_ADDRESS
    _STACK_ADDRESS = 1000

    _SAVED_DISPLACEMENT = 0 * _WORD_SIZE
    _RETURN_ADDRESS_DISPLACEMENT = 1 * _WORD_SIZE
    _VARIABLES_DISPLACEMENT = 2 * _WORD_SIZE

    def __init__(self):
        self.lookahead = None
        self.scopes = {}
        self.scope_numbers = set()
        self.symbol_table = SymbolTable()
        self.semantic_stack = []
        self.control_stack = []
        self.assembler = Assembler(self._DATA_ADDRESS, self._TEMP_ADDRESS, self._STACK_ADDRESS)
        self.routines: Dict[str, Any] = {
            '#declare': self.declare,
            '#declare_id': self.declare_id,
            '#declare_var': self.declare_var,
            '#declare_type': self.declare_type,
            '#declare_list': self.declare_list,
            '#declare_func': self.declare_func,
            '#cell_no': self.cell_no,
            '#arg_no': self.arg_no,
            '#add_scope': self.add_scope,
            '#release_scope': self.release_scope,
            '#pid': self.pid,
            '#pnum': self.pnum,
            '#assign': self.assign,
            '#displace': self.displace,
            '#save': self.save,
            '#pop': self.pop,
            '#jp': self.jp,
            '#jp_back': self.jp_back,
            '#jpf': self.jpf,
            '#jpf_save': self.jpf_save,
            '#break_label': self.break_label,
            '#label': self.label,
            '#repeat': self.repeat,
            '#break_assign': self.break_assign,
            '#relop': self.relop,
            '#cmp': self.cmp,
            '#pre_func': self.pre_func,
            '#skip': self.skip,
        }

    @property
    def pb_index(self):
        return len(self.assembler.program_block)

    @classmethod
    def indirect(cls, address):
        return '@%s' % address

    @classmethod
    def constant(cls, val):
        return '#%s' % val

    @classmethod
    def get_display_address(cls, scope):
        return cls._TEMP_ADDRESS + cls._WORD_SIZE + cls._WORD_SIZE * scope

    @classmethod
    def get_variable_displacement(cls, index):
        return cls._VARIABLES_DISPLACEMENT + cls._WORD_SIZE * index

    def get_temp_var(self):
        self.assembler.move_temp_pointer(self._WORD_SIZE)
        return self.assembler.temp_address - self._WORD_SIZE

    def ss_pop(self):
        return self.semantic_stack.pop()

    def ss_peek(self):
        return self.semantic_stack[-1]

    def cs_pop(self):
        return self.control_stack.pop()

    def cs_peek(self):
        return self.control_stack[-1]

    def ss_push(self, item):
        self.semantic_stack.append(item)

    def pb_insert(self, index, opcode, *args):
        self.assembler.add_instruction(index, opcode, *args)

    def cs_push(self, item):
        self.control_stack.append(item)

    def call(self, semantic_action, lookahead):
        self.lookahead = lookahead
        self.routines[semantic_action]()

    def declare(self):
        self.symbol_table.add_symbol()

    def declare_id(self, lookahead):
        self.symbol_table.set_id(lookahead)

    def declare_type(self, lookahead):
        self.symbol_table.set_type(lookahead)

    def declare_var(self):
        self.symbol_table.set_var(IDItem.IDVar.VARIABLE)

    def declare_list(self):
        self.symbol_table.set_var(IDItem.IDVar.ARRAY)

    def declare_func(self):
        self.symbol_table.set_var(IDItem.IDVar.FUNCTION)

    def cell_no(self, lookahead):
        self.symbol_table.set_cell_no(int(lookahead))

    def arg_count(self):
        self.symbol_table.increment_arg_count()

    def add_scope(self):
        self.symbol_table.add_scope()
        scope = self.symbol_table.current_scope.number
        if scope not in self.scope_numbers:
            display_address = self.get_display_address(scope)
            self.pb_insert(OPCode.ASSIGN, self.constant(-1), display_address)
            self.scope_numbers.add(scope)

    def release_scope(self):
        func_name = self.symbol_table.current_scope.name
        self.scopes[func_name] = self.symbol_table.pop()

    def pid(self, lookahead):
        self.ss_push(lookahead[1])

    def pnum(self, lookahead):
        self.ss_push(self.constant(lookahead[1]))

    def assign(self):
        rhs = self.ss_pop()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, rhs, self.indirect(self.ss_pop()))
        self.ss_push(rhs)

    def displace(self):
        displacement = self.ss_pop()
        self.pb_insert(self.pb_index, OPCode.ADD, displacement, self.ss_peek(), self.ss_peek())

    def save(self):
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def pop(self):
        self.ss_pop()

    def jp(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP, self.pb_index)

    def jp_back(self):
        self.pb_insert(self.pb_index, self.indirect(self.cs_pop()))
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def jpf(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), self.pb_index)

    def jpf_save(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), self.pb_index + 1)
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def break_label(self):
        temp = self.get_temp_var()
        self.cs_push(temp)

    def label(self):
        self.ss_push(self.pb_index)

    def repeat(self):
        self.pb_insert(self.pb_index, OPCode.JUMP_IF, self.ss_pop(), self.pb_index + 2)
        self.pb_insert(self.pb_index, OPCode.JUMP, self.ss_pop())

    def break_assign(self):
        self.pb_insert(self.ss_pop(), OPCode.ASSIGN, self.pb_index, self.cs_pop())

    def relop(self, lookahead):
        self.ss_push('LT' if lookahead[1] == '<' else 'EQ')

    def cmp(self):
        second_operand = self.ss_pop()
        operator = self.ss_pop()
        first_operand = self.ss_pop()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(temp)

    def addop(self, lookahead):
        self.ss_push('ADD' if lookahead[1]=='+' else 'SUB')

    def add(self):
        second_operand = self.ss_pop()
        operator = self.ss_pop()
        first_operand = self.ss_pop()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(temp)

    def mult(self):
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.MULT, self.ss_pop(), self.ss_pop(), temp)
        self.ss_push(temp)

    def pre_func(self):
        self.ss_push(self.pb_index)
        for _ in range(2):
            self.pb_insert(self.pb_index, OPCode.EMPTY)

    def skip(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP, self.pb_index)

    def set_call_address(self):
        self.symbol_table.set_call_address(self.pb_index - 1)

    def set_runtime_stack_top(self):
        displacement = self.symbol_table.current_scope_size
        self.pb_insert(self.ss_pop(), OPCode.ADD, self._RUNTIME_STACK_TOP, displacement, self._RUNTIME_STACK_TOP)
        self.pb_insert(self.pb_index, OPCode.SUB, self._RUNTIME_STACK_TOP, displacement, self._RUNTIME_STACK_TOP)

    def return_jp(self):
        scope = self.symbol_table.current_scope.number
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ADD, self.get_display_address(scope), self._RETURN_ADDRESS_DISPLACEMENT,
                       temp)
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(temp))

    def stmt_flag(self):
        self.ss_push("stmt_flag")

    def pop_stmt_flag(self):
        while self.ss_pop() != "stmt_flag":
            pass

    def break_jp(self):
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(self.cs_peek()))

    def apply_id(self):
        _id = self.ss_pop()
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            return

        scope, index = self.symbol_table.get_address()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
        self.pb_insert(self.pb_index, OPCode.ADD, temp, self.get_variable_displacement(index), temp)

        if var != IDItem.IDVar.ARRAY:
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.indirect(temp), temp)

        self.ss_push(temp)

    def assign_id(self):
        _id = self.ss_pop()
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            return

        scope, index = self.symbol_table.get_address()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
        self.pb_insert(self.pb_index, OPCode.ADD, temp, self.get_variable_displacement(index), temp)

        self.ss_push(temp)
