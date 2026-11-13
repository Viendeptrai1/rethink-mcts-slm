from typing import List, Union

def do_algebra(operator: List[str], operand: List[int]) -> int:
    """
    Given two lists operator, and operand. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operator['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '//': 2,
        '**': 3
    }

    def apply_op(a: int, b: int, op: str) -> int:
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '//':
            return a // b
        elif op == '**':
            return a ** b
        else:
            raise ValueError(f"Unsupported operator: {op}")

    values = [operand[0]]
    ops = []

    for i, op in enumerate(operator):
        while ops and precedence.get(ops[-1], 0) >= precedence.get(op, 0):
            val2 = values.pop()
            val1 = values.pop()
            op_top = ops.pop()
            values.append(apply_op(val1, val2, op_top))
        values.append(operand[i + 1])
        ops.append(op)

    while ops:
        val2 = values.pop()
        val1 = values.pop()
        op_top = ops.pop()
        values.append(apply_op(val1, val2, op_top))

    return values[0]