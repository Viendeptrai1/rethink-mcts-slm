def do_algebra(operator, operand):
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '//'):
            return 2
        if op == '**':
            return 3
        return 0

    def apply_operator(operators, values):
        right = values.pop()
        left = values.pop()
        op = operators.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '//':
            values.append(left // right)
        elif op == '**':
            values.append(left ** right)

    operators = []
    values = []
    i = 0

    while i < len(operand):
        values.append(operand[i])
        if i < len(operator):
            while (operators and precedence(operators[-1]) >= precedence(operator[i])):
                apply_operator(operators, values)
            operators.append(operator[i])
        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]