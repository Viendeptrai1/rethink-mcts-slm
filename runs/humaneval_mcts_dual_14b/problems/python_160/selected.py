def do_algebra(operators, operands):
    def apply_operator(ops, vals):
        right = vals.pop()
        left = vals.pop()
        op = ops.pop()
        if op == '+':
            vals.append(left + right)
        elif op == '-':
            vals.append(left - right)
        elif op == '*':
            vals.append(left * right)
        elif op == '//':
            vals.append(left // right)
        elif op == '**':
            vals.append(left ** right)

    precedence = {'+': 1, '-': 1, '*': 2, '//': 2, '**': 3}
    op_stack = []
    val_stack = []

    for i in range(len(operands)):
        val_stack.append(operands[i])
        if i < len(operators):
            while (op_stack and precedence[op_stack[-1]] >= precedence[operators[i]]):
                apply_operator(op_stack, val_stack)
            op_stack.append(operators[i])

    while op_stack:
        apply_operator(op_stack, val_stack)

    return val_stack[0]

# Example usage:
# operators = ['+', '*', '-']
# operands = [2, 3, 4, 5]
# result = do_algebra(operators, operands)
# print(result)  # Output: 9