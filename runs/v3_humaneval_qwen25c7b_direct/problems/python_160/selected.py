def do_algebra(operator, operand):
    from functools import reduce
    ops = {'+': lambda x, y: x + y,
           '-': lambda x, y: x - y,
           '*': lambda x, y: x * y,
           '//': lambda x, y: x // y,
           '**': lambda x, y: x ** y}
    return reduce(lambda acc, op: ops[op](acc, operand.pop(0)), operator, operand[0])