def do_algebra(operators, operands):
    """
    Given two lists operators, and operands. The first list has basic algebra operations, and 
    the second list is a list of integers. Use the two given lists to build the algebric 
    expression and return the evaluation of this expression.

    The basic algebra operations:
    Addition ( + ) 
    Subtraction ( - ) 
    Multiplication ( * ) 
    Floor division ( // ) 
    Exponentiation ( ** ) 

    Example:
    operators = ['+', '*', '-']
    operands = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operators list is equal to the length of operands list minus one.
        Operands is a list of non-negative integers.
        Operators list has at least one operator, and operands list has at least two operands.
    """
    # Start with the first operand
    result = operands[0]
    
    # Iterate over the operators and operands
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
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    
    return result

# Example usage:
# operators = ['+', '*', '-']
# operands = [2, 3, 4, 5]
# print(do_algebra(operators, operands))  # Output: 9