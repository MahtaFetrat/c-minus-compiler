from typing import Dict, Any

from src.code_gen.assembler import Assembler, OPCode
from src.code_gen.symbol_table import SymbolTable, IDItem


class CodeGen:
    _OUTPUT_FILENAME = "output.txt"
    _WORD_SIZE = 4
    _DATA_ADDRESS = 0
    _RUNTIME_STACK_TOP = 500
    _STACK_ADDRESS = _RUNTIME_STACK_TOP + 11 * _WORD_SIZE
    _TEMP_ADDRESS = 1000000012

    _SAVED_DISPLACEMENT = 0 * _WORD_SIZE
    _RETURN_ADDRESS_DISPLACEMENT = 1 * _WORD_SIZE
    _RETURN_VALUE_DISPLACEMENT = 2 * _WORD_SIZE
    _VARIABLES_DISPLACEMENT = 3 * _WORD_SIZE

    def __init__(self):
        self.lookahead = None
        self.symbol_table = SymbolTable()
        self.scopes = {"output": self.symbol_table.get_output_func_scope()}
        self.scope_numbers = {0, 1}
        self.semantic_stack = []
        self.control_stack = []
        self.assembler = Assembler(self._DATA_ADDRESS, self._TEMP_ADDRESS, self._STACK_ADDRESS, self._RUNTIME_STACK_TOP)
        self.arg_counts = []
        self.routines: Dict[str, Any] = {
            "#declare": self.declare,
            "#declare-ID": self.declare_id,
            "#declare-var": self.declare_var,
            "#declare-type": self.declare_type,
            "#declare-array": self.declare_array,
            "#declare-func": self.declare_func,
            "#cell-no": self.cell_no,
            "#add-scope": self.add_scope,
            "#release-scope": self.release_scope,
            "#pid": self.pid,
            "#pnum": self.pnum,
            "#assign": self.assign,
            "#displace": self.displace,
            "#save": self.save,
            "#save-3": self.save_3,
            "#jp": self.jp,
            "#break-jp": self.break_jp,
            "#jpf": self.jpf,
            "#jpf-save": self.jpf_save,
            "#break-label": self.break_label,
            "#label": self.label,
            "#repeat-jp": self.repeat_jp,
            "#break-assign": self.break_assign,
            "#relop": self.relop,
            "#cmp": self.cmp,
            "#skip": self.skip,
            "#set-call-address": self.set_call_address,
            "#set-runtime-stack-top": self.set_runtime_stack_top,
            "#retrieve-display": self.retrieve_display,
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
            "#set-args": self.set_args,
            "#update-displays": self.update_displays,
            "#initialize-arg-count": self.initialize_arg_count,
            "#func-call": self.func_call,
            "#increment-arg-no": self.increment_arg_no,
            "#init-return-val": self.init_return_val,
            "#save-return-val": self.save_return_val,
            "#get-return-val": self.get_return_val,
            "#pruntime-top": self.pruntime_top
        }

    @property
    def pb_index(self):
        return len(self.assembler.program_block)

    def indirect(self, address, pb_index):
        if str(address).startswith("@"):
            temp = self.get_temp_var()
            self.pb_insert(pb_index, OPCode.ASSIGN, address, temp)
            return "@%s" % temp
        return "@%s" % address

    @classmethod
    def constant(cls, val):
        return "#%s" % val

    @classmethod
    def runtime_temp(cls, val):
        return "^%s" % val

    @classmethod
    def get_display_address(cls, scope):
        return cls._RUNTIME_STACK_TOP + cls._WORD_SIZE + cls._WORD_SIZE * scope

    @classmethod
    def get_local_variable_displacement(cls, index):
        return cls._VARIABLES_DISPLACEMENT + cls._WORD_SIZE * index

    def get_temp_variable_displacement(self, scope, index):
        return self._VARIABLES_DISPLACEMENT + scope.local_variable_size(self._WORD_SIZE) + self._WORD_SIZE * index

    def get_data_address(self, index):
        return self._DATA_ADDRESS + self._WORD_SIZE * index

    def get_temp_var(self):
        self.assembler.move_temp_pointer(self._WORD_SIZE)
        return self.assembler.temp_address - self._WORD_SIZE

    def get_runtime_temp_var(self):
        temp = self.symbol_table.current_scope.temp_variables_count
        self.symbol_table.increment_temp_variables_count()
        return self.runtime_temp(temp)

    def convert_runtime_temp(self, item, scope, pb_index, display_address=None):
        if str(item).startswith("^"):
            temp = self.get_temp_var()
            self.pb_insert(pb_index, OPCode.ASSIGN, display_address if display_address else self.get_display_address(scope.number), temp)
            self.pb_insert(pb_index + 1, OPCode.ADD, self.constant(self.get_temp_variable_displacement(scope, int(str(item)[1:]))), temp, temp)
            return self.indirect(temp, pb_index)
        return None

    def ss_pop(self, pb_index, display_address=None):
        item = self.semantic_stack.pop()
        runtime_temp = self.convert_runtime_temp(item, self.symbol_table.current_scope, pb_index, display_address)
        return runtime_temp if runtime_temp else item

    def ss_peek(self, pb_index, index=1, display_address=None):
        item = self.semantic_stack[-index]
        runtime_temp = self.convert_runtime_temp(item, self.symbol_table.current_scope, pb_index, display_address)
        return runtime_temp if runtime_temp else item

    def cs_pop(self):
        return self.control_stack.pop()

    def cs_peek(self):
        return self.control_stack[-1]

    def ss_push(self, item):
        self.semantic_stack.append(item)

    def arg_counts_pop(self):
        return self.arg_counts.pop()

    def arg_counts_peek(self):
        return self.arg_counts[-1]

    def pb_insert(self, index, opcode, *args):
        self.assembler.add_instruction(index, opcode, *args)

    def cs_push(self, item):
        self.control_stack.append(item)

    def call(self, semantic_action, lookahead):
        self.lookahead = lookahead[1]
        print(self.pb_index, end=". ")
        print(self.symbol_table.current_scope.name, end="|")
        print(semantic_action, end=': ')
        print(self.semantic_stack, end=" ")
        print(self.control_stack, end=' ')
        print(self.arg_counts)
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
        rhs = self.ss_pop(self.pb_index)
        var = self.ss_pop(self.pb_index)
        indirect = self.indirect(var, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, rhs, indirect)
        self.ss_push(rhs)

    def displace(self, lookahead):
        displacement = self.ss_pop(self.pb_index)
        scope = self.symbol_table.current_scope
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), scope, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.MULT, displacement, self.constant(4), temp)
        op = self.ss_peek(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ADD, temp, op, op)

    def save(self, lookahead):
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def save_3(self, lookahead):
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)
        self.pb_insert(self.pb_index, OPCode.EMPTY)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def jp(self, lookahead):
        self.pb_insert(self.ss_pop(self.pb_index), OPCode.JUMP, self.pb_index)

    def jp_back(self, lookahead):
        self.pb_insert(self.pb_index, self.indirect(self.cs_pop()))
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def jpf(self, lookahead):
        index = self.ss_pop(self.pb_index)
        condition = self.ss_pop(index)
        self.pb_insert(index + 2, OPCode.JUMP_FALSE, condition, self.pb_index)

    def jpf_save(self, lookahead):
        index = self.ss_pop(self.pb_index)
        condition = self.ss_pop(index)
        self.pb_insert(index + 2, OPCode.JUMP_FALSE, condition, self.pb_index + 1)
        self.ss_push(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.EMPTY)

    def break_label(self, lookahead):
        temp = self.get_temp_var()
        self.cs_push(temp)

    def label(self, lookahead):
        self.ss_push(self.pb_index)

    def repeat_jp(self, lookahead):
        condition = self.ss_pop(self.pb_index)
        label = self.ss_pop(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.JUMP_FALSE, condition, label)

    def break_assign(self, lookahead):
        self.pb_insert(self.ss_pop(self.pb_index), OPCode.ASSIGN, self.constant(self.pb_index), self.cs_pop())

    def relop(self, lookahead):
        self.ss_push("LT" if lookahead == "<" else "EQ")

    def cmp(self, lookahead):
        second_operand = self.ss_pop(self.pb_index)
        operator = self.ss_pop(self.pb_index)
        first_operand = self.ss_pop(self.pb_index)
        scope = self.symbol_table.current_scope

        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, scope, self.pb_index)
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(runtime_temp)

    def addop(self, lookahead):
        self.ss_push("ADD" if lookahead == "+" else "SUB")

    def add(self, lookahead):
        second_operand = self.ss_pop(self.pb_index)
        operator = self.ss_pop(self.pb_index)
        first_operand = self.ss_pop(self.pb_index)
        scope = self.symbol_table.current_scope

        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, scope, self.pb_index)
        self.pb_insert(self.pb_index, OPCode(operator), first_operand, second_operand, temp)
        self.ss_push(runtime_temp)

    def mult(self, lookahead):
        scope = self.symbol_table.current_scope

        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, scope, self.pb_index)
        op1 = self.ss_pop(self.pb_index)
        op2 = self.ss_pop(self.pb_index)
        self.pb_insert(self.pb_index, OPCode.MULT, op1, op2, temp)
        self.ss_push(runtime_temp)

    def pre_func(self, lookahead):
        self.ss_push(self.pb_index)
        for _ in range(2):
            self.pb_insert(self.pb_index, OPCode.EMPTY)

    def skip(self, lookahead):
        self.pb_insert(self.ss_pop(self.pb_index), OPCode.JUMP, self.pb_index)

    def set_call_address(self, lookahead):
        self.symbol_table.set_call_address(self.pb_index - 1)

    def set_runtime_stack_top(self, lookahead):
        displacement = self.get_runtime_mem_size(self.symbol_table.current_scope)
        self.pb_insert(
            self.ss_pop(self.pb_index),
            OPCode.ADD,
            self._RUNTIME_STACK_TOP,
            self.constant(displacement),
            self._RUNTIME_STACK_TOP,
        )
        self.pb_insert(
            self.pb_index,
            OPCode.SUB,
            self._RUNTIME_STACK_TOP,
            self.constant(displacement),
            self._RUNTIME_STACK_TOP,
        )

    def retrieve_display(self, lookahead):
        return_value = self.ss_pop(self.pb_index)
        scope = self.get_function_scope(self.ss_pop(self.pb_index))
        self.ss_push(return_value)

        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), self.symbol_table.current_scope, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ASSIGN,
            self.get_display_address(scope.number),
            temp
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ASSIGN,
            temp_indirect,
            self.get_display_address(scope.number),
        )

    def return_jp(self, lookahead):
        scope = self.symbol_table.current_scope
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), scope, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_ADDRESS_DISPLACEMENT),
            temp,
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, temp_indirect, temp)
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.JUMP, temp_indirect)

    def stmt_flag(self, lookahead):
        self.ss_push("stmt_flag")

    def pop_stmt_flag(self, lookahead):
        while self.ss_pop(self.pb_index) != "stmt_flag":
            pass

    def break_jp(self, lookahead):
        self.pb_insert(self.pb_index, OPCode.JUMP, self.indirect(self.cs_peek(), self.pb_index))

    def apply_id(self, lookahead):
        _id = self.ss_pop(self.pb_index)
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            self.ss_push(_id)
            return

        scope, index = self.get_address(_id)
        args_count = scope.args_count
        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, self.symbol_table.current_scope, self.pb_index)
        scope = scope.number
        if scope != 0:
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
            self.pb_insert(self.pb_index, OPCode.ADD, temp, self.constant(self.get_local_variable_displacement(index)), temp)

            if var == IDItem.IDVar.ARRAY and index < args_count:
                temp_indirect = self.indirect(temp, self.pb_index)
                self.pb_insert(self.pb_index, OPCode.ASSIGN, temp_indirect, temp)
            if var != IDItem.IDVar.ARRAY:
                temp_indirect = self.indirect(temp, self.pb_index)
                self.pb_insert(self.pb_index, OPCode.ASSIGN, temp_indirect, temp)
        else:
            if var != IDItem.IDVar.ARRAY:
                self.pb_insert(self.pb_index, OPCode.ASSIGN, index, temp)
            else:
                self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(index), temp)

        self.ss_push(runtime_temp)

    def assign_id(self, lookahead):
        _id = self.ss_pop(self.pb_index)
        var = self.symbol_table.get_id_var(_id)

        if var == IDItem.IDVar.FUNCTION:
            self.ss_push(_id)
            return

        scope, index = self.get_address(_id)
        args_count = scope.args_count
        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, self.symbol_table.current_scope, self.pb_index)
        scope = scope.number
        if scope != 0:
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope), temp)
            self.pb_insert(self.pb_index, OPCode.ADD, temp, self.constant(self.get_local_variable_displacement(index)), temp)
            if var == IDItem.IDVar.ARRAY and index < args_count:
                temp_indirect = self.indirect(temp, self.pb_index)
                self.pb_insert(self.pb_index, OPCode.ASSIGN, temp_indirect, temp)
        else:
            self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(index), temp)

        self.ss_push(runtime_temp)

    def update_displays(self, lookahead):
        arg_count = self.arg_counts_peek()
        scope = self.get_function_scope(self.ss_peek(self.pb_index, arg_count + 2))

        ar_temp = self.convert_runtime_temp(self.get_runtime_temp_var(), self.symbol_table.current_scope, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope.number), ar_temp)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self._RUNTIME_STACK_TOP, self.get_display_address(scope.number))

        cmp_temp = self.convert_runtime_temp(self.get_runtime_temp_var(), self.symbol_table.current_scope, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.LESS, self.constant(0), ar_temp, cmp_temp)
        self.pb_insert(self.pb_index, OPCode.JUMP_FALSE, cmp_temp, self.pb_index + 2)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, ar_temp, self.indirect(self._RUNTIME_STACK_TOP, self.pb_index))

    def initialize_arg_count(self, lookahead):
        self.arg_counts.append(0)

    def func_call(self, lookahead):
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), self.symbol_table.current_scope, self.pb_index)

        scope = self.get_function_scope(self.ss_peek(self.pb_index))
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_ADDRESS_DISPLACEMENT),
            temp,
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(self.pb_index + 2), temp_indirect)
        self.pb_insert(self.pb_index, OPCode.JUMP, scope.call_address)

    def get_indirect_value(self, lookahead):
        ss_top = self.ss_peek(self.pb_index)
        op = self.indirect(ss_top, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, op, ss_top)

    def pruntime_top(self, lookahead):
        temp = self.get_temp_var()
        scope = self.symbol_table.current_scope
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.get_display_address(scope.number), temp)
        self.ss_push(temp)

    def set_args(self, lookahead):
        arg_count = self.arg_counts_pop()
        display_address = self.ss_pop(self.pb_index)
        scope = self.get_function_scope(self.ss_peek(self.pb_index, arg_count + 1))
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), self.symbol_table.current_scope, self.pb_index)
        for arg_no in range(arg_count, 0, -1):
            self.pb_insert(
                self.pb_index,
                OPCode.ADD,
                self.get_display_address(scope.number),
                self.constant(self.get_local_variable_displacement(arg_no - 1)),
                temp
            )
            op = self.ss_pop(self.pb_index, display_address)
            temp_indirect = self.indirect(temp, self.pb_index)
            self.pb_insert(self.pb_index, OPCode.ASSIGN, op, temp_indirect)

    def increment_arg_no(self, lookahead):
        self.arg_counts[-1] = self.arg_counts[-1] + 1

    def init_return_val(self, lookahead):
        scope = self.symbol_table.current_scope
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), scope, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_VALUE_DISPLACEMENT),
            temp,
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(0), temp_indirect)

    def save_return_val(self, lookahead):
        scope = self.symbol_table.current_scope
        temp = self.convert_runtime_temp(self.get_runtime_temp_var(), scope, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_VALUE_DISPLACEMENT),
            temp,
        )
        op = self.ss_pop(self.pb_index)
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, op, temp_indirect)

    def get_return_val(self, lookahead):
        scope = self.get_function_scope(self.ss_peek(self.pb_index))

        runtime_temp = self.get_runtime_temp_var()
        temp = self.convert_runtime_temp(runtime_temp, self.symbol_table.current_scope, self.pb_index)
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_VALUE_DISPLACEMENT),
            temp,
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, temp_indirect, temp)
        self.ss_push(runtime_temp)

    def get_function_scope(self, function_name):
        if function_name in self.scopes:
            return self.scopes[function_name]
        return self.symbol_table.get_function_scope(function_name)

    def get_address(self, _id):
        scope, index = self.symbol_table.get_address(_id)
        if scope.number == 0:
            return scope, self.get_data_address(index)
        return scope, index

    def get_runtime_mem_size(self, scope):
        return scope.variable_size(self._WORD_SIZE) + self._VARIABLES_DISPLACEMENT

    def insert_main_call(self):
        scope = self.get_function_scope("main")
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self._RUNTIME_STACK_TOP, self.get_display_address(scope.number))

        temp = self.get_temp_var()
        self.pb_insert(
            self.pb_index,
            OPCode.ADD,
            self.get_display_address(scope.number),
            self.constant(self._RETURN_ADDRESS_DISPLACEMENT),
            temp,
        )
        temp_indirect = self.indirect(temp, self.pb_index)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(self.pb_index + 2), temp_indirect)
        self.pb_insert(self.pb_index, OPCode.JUMP, scope.call_address)
        self.pb_insert(self.pb_index, OPCode.ASSIGN, self.constant(0), self.get_temp_var())

    def close(self):
        self.insert_main_call()
        with open(self._OUTPUT_FILENAME, "w") as f:
            f.write(self.assembler.code)
