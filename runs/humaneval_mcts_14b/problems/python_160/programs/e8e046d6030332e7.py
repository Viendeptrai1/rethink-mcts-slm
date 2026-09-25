def do_algebra(operators, operands):
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '//'):
            return 2
        if op == '**':
            return 3
        return 0

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '//':
            values.append(left // right)
        elif operator == '**':
            values.append(left ** right)

    def greater_precedence(op1, op2):
        return precedence(op1) > precedence(op2)

    values = []
    ops = []

    for i in range(len(operands)):
        values.append(operands[i])
        if i < len(operators):
            while (ops and greater_precedence(ops[-1], operators[i])):
                apply_operator(ops, values)
            ops.append(operators[i])

    while ops:
        apply_operator(ops, values)

    return values[0]

# Example usage:
# operators = ['+', '*', '-']
# operands = [2, 3, 4, 5]
# print(do_algebra(operators, operands))  # Output: 9