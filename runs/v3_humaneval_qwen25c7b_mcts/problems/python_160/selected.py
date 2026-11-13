def do_algebra(operator, operand):
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
        precedence = {'+': 1, '-': 1, '*': 2, '//': 2, '**': 3}
        return precedence[op1] > precedence[op2]

    operators = []
    values = []

    for i in range(len(operand)):
        values.append(operand[i])
        if i < len(operator):
            while (operators and operators[-1] != '(' and
                   greater_precedence(operators[-1], operator[i])):
                apply_operator(operators, values)
            operators.append(operator[i])

    while operators:
        apply_operator(operators, values)

    return values[0]