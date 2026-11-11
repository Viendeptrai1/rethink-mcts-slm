def do_algebra(operators, operands):
    # Start with the first operand
    result = operands[0]
    
    # Iterate over the operators and corresponding operands
    for i, operator in enumerate(operators):
        if operator == '+':
            result += operands[i + 1]
        elif operator == '-':
            result -= operands[i + 1]
        elif operator == '*':
            result *= operands[i + 1]
        elif operator == '//':
            result //= operands[i + 1]
        elif operator == '**':
            result **= operands[i + 1]
    
    return result