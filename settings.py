from enum import Enum


class op_types(Enum):
    integral = "integral"
    derivative = "derivative"
    matrix_op = "matrix operation"
    de = "de"

class keys(Enum):
    type = "type"
    function = "function"
    var = "var"
    order = "order"
    lower = "lower"
    upper = "upper"
    left_function = "left_function"
    right_function = "right_function"
    op = "op"
    first = "first"
    second = "second"