from typing import Dict, Any

from src.code_gen.assembler import Assembler, OPCode
from src.code_gen.symbol_table import SymbolTable, IDItem


class CodeGen:
    _WORD_SIZE = 4
    _DATA_ADDRESS = 100
    _TEMP_ADDRESS = 500
    _RUNTIME_STACK_TOP = _TEMP_ADDRESS
    _STACK_ADDRESS = 1000

    _SAVED_INDEX = 0
    _RETURN_ADDRESS_INDEX = 1

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

    def get_temp_var(self):
        self.assembler.move_temp_pointer(self._WORD_SIZE)
        return self.assembler.temp_address - self._WORD_SIZE

    def ss_pop(self):
        return self.semantic_stack.pop()

    def cs_pop(self):
        return self.control_stack.pop()

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

    def pid(self):
        self.ss_push(self.lookahead[1])

    def pnum(self):
        self.ss_push(f'#{self.lookahead[1]}')

    def assign(self):
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.ss_pop(), self.ss_pop())
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def displace(self):
        temp = self.ss_pop() + self.semantic_stack[-1]
        self.semantic_stack.append(temp)

    def save(self):
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def pop(self):
        self.ss_pop()

    def jp(self):
        self.pb_insert(self.pb_index, OPCode.JUMP, self.ss_pop())
        self.pb_insert(self.pb_index, OPCode.JUMP, self.ss_pop())

    def jp_back(self):
        self.pb_insert(self.pb_index, self.indirect(self.cs_pop()))
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def jpf(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), len(self.ss_pop()))

    def jpf_save(self):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), len(self.ss_pop()) + 1)
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def break_label(self):
        temp = self.get_temp_var()
        self.cs_push(temp)

    def label(self):
        self.ss_push(self.pb_index)

    def repeat(self):
        self.pb_insert(self.pb_index, OPCode.JUMP, self.ss_pop(), self.ss_pop())

    def break_assign(self):
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.pb_index, self.cs_pop())

    def relop(self):
        self.ss_push('LT' if self.lookahead[1] == '<' else 'EQ')

    def cmp(self):
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, self.semantic_stack[-2], self.semantic_stack[-1], self.semantic_stack[-3], temp)
        for _ in range(3):
            self.ss_pop()
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
        t = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ADD, self.get_display_address(scope), self._RETURN_ADDRESS_INDEX, t)
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(t))
