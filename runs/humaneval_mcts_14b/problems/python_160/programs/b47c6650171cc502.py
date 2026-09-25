def do_algebra(operator, operand):
    # Initialize the result with the first operand
    result = operand[0]
    
    # Iterate through the operators and operands simultaneously
    for i, op in enumerate(operator):
        if op == '+':
            result += operand[i + 1]
        elif op == '-':
            result -= operand[i + 1]
        elif op == '*':
            result *= operand[i + 1]
        elif op == '//':
            result //= operand[i + 1]
        elif op == '**':
            result **= operand[i + 1]
    
    return result