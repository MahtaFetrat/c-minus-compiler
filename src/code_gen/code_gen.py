from typing import Dict, Any

from src.code_gen.assembler import Assembler, OPCode
from src.code_gen.symbol_table import SymbolTable


class CodeGen:
    _WORD_SIZE = 4
    _DATA_ADDRESS = 100
    _TEMP_ADDRESS = 500
    _STACK_ADDRESS = 1000

    def __init__(self):
        self.lookahead = None
        self.scopes = {}
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

    def get_temp_var(self):
        self.assembler.move_temp_pointer(self._WORD_SIZE)
        return self.assembler.temp_address - self._WORD_SIZE

    def ss_pop(self):
        return self.semantic_stack.pop()

    def cs_pop(self):
        return self.control_stack.pop()

    def ss_push(self, item):
        self.semantic_stack.append(item)

    def pb_insert(self, *args):
        self.assembler.add_instruction(*args)

    def cs_push(self, item):
        self.control_stack.append(item)

    def call(self, semantic_action, lookahead):
        self.lookahead = lookahead
        self.routines[semantic_action]()

    def declare(self):
        pass

    def declare_id(self):
        pass

    def declare_var(self):
        pass

    def declare_type(self):
        pass

    def declare_list(self):
        pass

    def declare_func(self):
        pass

    def cell_no(self):
        pass

    def arg_no(self):
        pass

    def add_scope(self):
        pass

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
        pass
