from typing import Dict, Any

from src.code_gen.assembler import Assembler, OPCode
from src.code_gen.symbol_table import SymbolTable, IDItem, Scope


class CodeGen:
    _OUTPUT_FILENAME = "output.txt"
    _WORD_SIZE = 4
    _DATA_ADDRESS = 100
    _RUNTIME_STACK_TOP = 500
    _TEMP_ADDRESS = _RUNTIME_STACK_TOP + 11 * _WORD_SIZE
    _STACK_ADDRESS = 1000

    _SAVED_DISPLACEMENT = 0 * _WORD_SIZE
    _RETURN_ADDRESS_DISPLACEMENT = 1 * _WORD_SIZE
    _RETURN_VALUE_DISPLACEMENT = 2 * _WORD_SIZE
    _VARIABLES_DISPLACEMENT = 3 * _WORD_SIZE

    def __init__(self):
        self.lookahead = None
        self.symbol_table = SymbolTable()
        self.scopes = {"output": self.symbol_table.get_output_func_scope()}
        self.scope_numbers = {1}
        self.semantic_stack = []
        self.control_stack = []
        self.assembler = Assembler(self._DATA_ADDRESS, self._TEMP_ADDRESS, self._STACK_ADDRESS, self._RUNTIME_STACK_TOP)
        self.arg_no = 0
        self.routines: Dict[str, Any] = {
            "#declare": self.declare,
            "#declare-ID": self.declare_id,
            "#declare-var": self.declare_var,
            "#declare-type": self.declare_type,
            "#declare-array": self.declare_array,
            "#declare-func": self.declare_func,
            "#cell-no": self.cell_no,
            "#arg-no": self.arg_no,
            "#add-scope": self.add_scope,
            "#release-scope": self.release_scope,
            "#pid": self.pid,
            "#pnum": self.pnum,
            "#assign": self.assign,
            "#displace": self.displace,
            "#save": self.save,
            "#pop": self.pop,
            "#jp": self.jp,
            "#break-jp": self.break_jp,
            "#jpf": self.jpf,
            "#jpf-save": self.jpf_save,
            "#break-label": self.break_label,
            "#label": self.label,
            "#repeat": self.repeat,
            "#break-assign": self.break_assign,
            "#relop": self.relop,
            "#cmp": self.cmp,
            "#skip": self.skip,
            "#set-call-address": self.set_call_address,
            "#set-runtime-stack-top": self.set_runtime_stack_top,
            "#return-jp": self.return_jp,
            "#arg-count": self.arg_count,
            "#stmt-flag": self.stmt_flag,
            "#pop-stmt-flag": self.pop_stmt_flag,
            "#assign-id": self.assign_id,
            "#apply-id": self.apply_id,
            "#get-indirect-value": self.get_indirect_value,
            "#addop": self.addop,
            "#add": self.add,
            "#mult": self.mult,
            "#update-displays": self.update_displays,
            "#reset-arg-no": self.reset_arg_no,
            "#func-call": self.func_call,
            "#set-arg": self.set_arg,
            "#save-return-val": self.save_return_val,
            "#get-return-val": self.get_return_val
        }

    @property
    def pb_index(self):
        return len(self.assembler.program_block)

    @classmethod
    def indirect(cls, address):
        return "@%s" % address

    @classmethod
    def constant(cls, val):
        return "#%s" % val

    @classmethod
    def get_display_address(cls, scope):
        return cls._RUNTIME_STACK_TOP + cls._WORD_SIZE + cls._WORD_SIZE * scope

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
        self.lookahead = lookahead[1]
        self.routines[semantic_action](self.lookahead)

    def declare(self, lookahead):
        self.symbol_table.add_symbol()

    def declare_id(self, lookahead):
        self.symbol_table.set_id(lookahead)

    def declare_type(self, lookahead):
        self.symbol_table.set_type(lookahead)

    def declare_var(self, lookahead):
        self.symbol_table.set_var(IDItem.IDVar.VARIABLE)

    def declare_array(self, lookahead):
        self.symbol_table.set_var(IDItem.IDVar.ARRAY)

    def declare_func(self, lookahead):
        self.symbol_table.set_var(IDItem.IDVar.FUNCTION)

    def cell_no(self, lookahead):
        self.symbol_table.set_cell_no(int(lookahead))

    def arg_count(self, lookahead):
        self.symbol_table.increment_arg_count()

    def add_scope(self, lookahead):
        self.symbol_table.add_scope()
        scope = self.symbol_table.current_scope.number
        if scope not in self.scope_numbers:
            display_address = self.get_display_address(scope)
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(-1), display_address)
            self.scope_numbers.add(scope)

    def release_scope(self, lookahead):
        func_name = self.symbol_table.current_scope.name
        self.scopes[func_name] = self.symbol_table.pop()

    def pid(self, lookahead):
        self.ss_push(lookahead)

    def pnum(self, lookahead):
        self.ss_push(self.constant(lookahead))

    def assign(self, lookahead):
        rhs = self.ss_pop()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, rhs, self.indirect(self.ss_pop()))
        self.ss_push(rhs)

    def displace(self, lookahead):
        displacement = self.ss_pop()
        self.pb_insert(self.pb_index, OPCode.ADD, displacement, self.ss_peek(), self.ss_peek())

    def save(self, lookahead):
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def pop(self, lookahead):
        self.ss_pop()

    def jp(self, lookahead):
        self.pb_insert(self.ss_pop(), OPCode.JUMP, self.pb_index)

    def jp_back(self, lookahead):
        self.pb_insert(self.pb_index, self.indirect(self.cs_pop()))
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def jpf(self, lookahead):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), self.pb_index)

    def jpf_save(self, lookahead):
        self.pb_insert(self.ss_pop(), OPCode.JUMP_IF, self.ss_pop(), self.pb_index + 1)
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def break_label(self, lookahead):
        temp = self.get_temp_var()
        self.cs_push(temp)

    def label(self, lookahead):
        self.ss_push(self.pb_index)

    def repeat(self, lookahead):
        self.pb_insert(self.pb_index, OPCode.JUMP_IF, self.ss_pop(), self.pb_index + 2)
        self.pb_insert(self.pb_index, OPCode.JUMP, self.ss_pop())

    def break_assign(self, lookahead):
        self.pb_insert(self.ss_pop(), OPCode.ASSIGN, self.pb_index, self.cs_pop())

    def relop(self, lookahead):
        self.ss_push("LT" if lookahead == "<" else "EQ")

    def cmp(self, lookahead):
        second_operand = self.ss_pop()
        operator = self.ss_pop()
        first_operand = self.ss_pop()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(temp)

    def addop(self, lookahead):
        self.ss_push("ADD" if lookahead == "+" else "SUB")

    def add(self, lookahead):
        second_operand = self.ss_pop()
        operator = self.ss_pop()
        first_operand = self.ss_pop()
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(temp)

    def mult(self, lookahead):
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.MULT, self.ss_pop(), self.ss_pop(), temp)
        self.ss_push(temp)

    def pre_func(self, lookahead):
        self.ss_push(self.pb_index)
        for _ in range(2):
            self.pb_insert(self.pb_index, OPCode.EMPTY)

    def skip(self, lookahead):
        self.pb_insert(self.ss_pop(), OPCode.JUMP, self.pb_index)

    def set_call_address(self, lookahead):
        self.symbol_table.set_call_address(self.pb_index - 1)

    def set_runtime_stack_top(self, lookahead):
        displacement = self._WORD_SIZE * self.symbol_table.current_scope_size + self._VARIABLES_DISPLACEMENT
        self.pb_insert(self.ss_pop(), OPCode.ADD, self._RUNTIME_STACK_TOP, displacement, self._RUNTIME_STACK_TOP)
        self.pb_insert(self.pb_index, OPCode.SUB, self._RUNTIME_STACK_TOP, displacement, self._RUNTIME_STACK_TOP)

    def return_jp(self, lookahead):
        scope = self.symbol_table.current_scope.number
        temp = self.get_temp_var()
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope),
            self._RETURN_ADDRESS_DISPLACEMENT,
            temp,
        )
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.indirect(temp), temp)
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(temp))

    def stmt_flag(self, lookahead):
        self.ss_push("stmt_flag")

    def pop_stmt_flag(self, lookahead):
        while self.ss_pop() != "stmt_flag":
            pass

    def break_jp(self, lookahead):
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(self.cs_peek()))

    def apply_id(self, lookahead):
        _id = self.ss_pop()
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            self.ss_push(_id)
            return

        scope, index = self.symbol_table.get_address(_id)
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
        self.pb_insert(self.pb_index, OPCode.ADD, temp, self.get_variable_displacement(index), temp)

        if var != IDItem.IDVar.ARRAY:
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.indirect(temp), temp)

        self.ss_push(temp)

    def assign_id(self, lookahead):
        _id = self.ss_pop()
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            self.ss_push(_id)
            return

        scope, index = self.symbol_table.get_address(_id)
        temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
        self.pb_insert(self.pb_index, OPCode.ADD, temp, self.get_variable_displacement(index), temp)

        self.ss_push(temp)

    def update_displays(self, lookahead):
        scope, index = self.symbol_table.get_address(self.ss_peek())

        ar_temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), ar_temp)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self._RUNTIME_STACK_TOP, self.get_display_address(scope))

        cmp_temp = self.get_temp_var()
        self.pb_insert(self.pb_index, OPCode.LESS, ar_temp, self.constant(0), cmp_temp)
        self.pb_insert(self.pb_index, OPCode.JUMP_IF, cmp_temp, self.pb_index + 2)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, ar_temp, self.indirect(self._RUNTIME_STACK_TOP))

    def reset_arg_no(self, lookahead):
        self.arg_no = 0

    def func_call(self, lookahead):
        scope = self.get_function_scope(self.ss_peek())

        temp = self.get_temp_var()
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self._RETURN_ADDRESS_DISPLACEMENT,
            temp,
        )
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.pb_index + 2, self.indirect(temp))
        self.pb_insert(self.pb_index, OPCode.JUMP, scope.call_address)

    def get_indirect_value(self, lookahead):
        ss_top = self.ss_pop()
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.indirect(ss_top), ss_top)

    def set_arg(self, lookahead):
        arg = self.ss_pop()
        scope = self.get_function_scope(self.ss_peek())

        temp = self.get_temp_var()
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.get_variable_displacement(self.arg_no),
            temp,
        )
        self.pb_insert(self.pb_index, OPCode.ASSIGN, arg, self.indirect(temp))

        self.arg_no = self.arg_no + 1

    def save_return_val(self, lookahead):
        temp = self.get_temp_var()
        scope = self.symbol_table.current_scope.number
        self.pb_insert(
            self.pb_index, OPCode.ADD, self.get_display_address(scope), self._RETURN_VALUE_DISPLACEMENT, temp,
        )
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.ss_pop(), self.indirect(temp))

    def get_return_val(self, lookahead):
        scope = self.get_function_scope(self.ss_pop())

        temp = self.get_temp_var()
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self._RETURN_VALUE_DISPLACEMENT,
            temp,
        )
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.indirect(temp), temp)
        self.ss_push(temp)

    def get_function_scope(self, function_name):
        if function_name in self.scopes:
            return self.scopes[function_name]
        return self.symbol_table.get_function_scope(function_name)

    def close(self):
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(0), self.get_temp_var())
        print(self.assembler.code)
        with open(self._OUTPUT_FILENAME, "w") as f:
            f.write(self.assembler.code)
