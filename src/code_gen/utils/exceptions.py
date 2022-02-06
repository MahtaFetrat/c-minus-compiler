class SemanticException(Exception):

    def __init__(self, lookahead=None, arg_no=None, expected_type=None, actual_type=None):
        super().__init__()
        self._lookahead = lookahead
        self._arg_no = arg_no
        self._expected_type = expected_type
        self._actual_type = actual_type

    def __str__(self):
        raise NotImplementedError


class BreakException(SemanticException):

    def __str__(self):
        return f"No 'repeat ... until' found for 'break'."


class VoidTypeException(SemanticException):

    def __str__(self):
        return f"Illegal type of void for '{self._lookahead}'."


class ScopingException(SemanticException):

    def __str__(self):
        return f"'{self._lookahead}' is not defined."


class ParameterNumber(SemanticException):

    def __str__(self):
        return f"Mismatch in numbers of arguments of '{self._lookahead}'."


class ParameterType(SemanticException):

    def __str__(self):
        return f"Mismatch in type of argument {self._arg_no} of '{self._lookahead}'. " \
               f"Expected '{self._expected_type}' but got '{self._actual_type}' instead."


class TypeMismatch(SemanticException):

    def __str__(self):
        return f"Type mismatch in operands, Got {self._actual_type} instead of int."