from typing import Dict, Any

from src.code_gen.assembler import Assembler
from src.code_gen.symbol_table import SymbolTable


class CodeGen:
    _WORD_SIZE = 4
    _DATA_ADDRESS = 100
    _TEMP_ADDRESS = 500
    _STACK_ADDRESS = 1000

    def __init__(self):
        self.pb_index = 0
        self.lookahead = None
        self.symbol_table = SymbolTable()
        self.program_block = []
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

    def get_temp_var(self):
        self.assembler.move_temp_pointer(self._WORD_SIZE)
        return self.assembler.temp_address - self._WORD_SIZE

    def ss_pop(self):
        return self.semantic_stack.pop()

    def cs_pop(self):
        return self.control_stack.pop()

    def ss_push(self, item):
        self.semantic_stack.append(item)

    def pb_push(self, item):
        self.program_block.append(item)

    def cs_add(self, item):
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
        pass

    def pid(self):
        pass

    def pnum(self):
        self.ss_push(f'#{self.lookahead[1]}')

    def assign(self):
        self.pb_push(f'(ASSIGN, {self.ss_pop()}, {self.ss_pop()}, ')
        self.pb_push('')

    def displace(self):
        temp = self.ss_pop() + self.semantic_stack[-1]
        self.semantic_stack.append(temp)

    def save(self):
        self.ss_push(len(self.program_block))

    def pop(self):
        self.ss_pop()

    def jp(self):
        self.pb_push(f'(JP, {self.semantic_stack.pop()}, , )')

    def jp_back(self):
        self.pb_push(f'(JP, @{self.control_stack.pop()}, , )')
        self.pb_push('')

    def jpf(self):
        self.program_block[
            self.ss_pop()
        ] = f'(JPF, {self.ss_pop()}, {len(self.ss_pop())}, )'

    def jpf_save(self):
        self.program_block[
            self.ss_pop()
        ] = f'(JPF, {self.ss_pop()}, {len(self.program_block) + 1}, )'
        self.ss_push(len(self.program_block))
        self.pb_push('')

    def break_label(self):
        temp = self.get_temp_var()
        self.cs_add(temp)

    def label(self):
        self.ss_push(len(self.program_block))

    def repeat(self):
        self.program_block.append(f'(JPF, {self.ss_pop()}, {self.ss_pop()}, )')

    def break_assign(self):
        self.program_block[
            self.ss_pop()
        ] = f'(ASSIGN, {len(self.program_block)}, {self.cs_pop()}, )'

    def relop(self):
        self.ss_push('LT' if self.lookahead[1] == '<' else 'EQ')

    def cmp(self):
        temp = self.get_temp_var()
        self.pb_push(f'({self.semantic_stack[-2]}, {self.semantic_stack[-1]}, {self.semantic_stack[-3]}, {temp})')
        for _ in range(3):
            self.ss_pop()
        self.ss_push(temp)

    def pre_func(self):
        self.ss_push(len(self.program_block))
        for _ in range(2):
            self.program_block.append('')

    def skip(self):
        pass
