def do_algebra(operator, operand):
    # Validate input lengths
    if len(operator) != len(operand) - 1:
        raise ValueError("The length of operator list must be one less than the length of operand list.")
    
    # Initialize result with the first operand
    result = operand[0]
    
    # Define a dictionary to map operators to their corresponding functions
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '//': lambda x, y: x // y,
        '**': lambda x, y: x ** y
    }
    
    # Iterate through the operators and operands
    for i, op in enumerate(operator):
        if op not in operations:
            raise ValueError(f"Invalid operator: {op}")
        
        # Apply the operation
        result = operations[op](result, operand[i + 1])
    
    return result