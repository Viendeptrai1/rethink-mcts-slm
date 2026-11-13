def do_algebra(operator, operand):
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
    # We need to evaluate the expression respecting operator precedence.
    # Precedence: ** > * / // > + -
    # Since the input is a flat list of operators and operands in order,
    # we can use two stacks: one for values and one for operators.
    # Or, since the expression is linear, we can process it by handling higher precedence first.
    
    # Approach:
    # 1. Create a list of tokens: [operand[0], op[0], operand[1], op[1], ..., operand[n]]
    # 2. Use a shunting-yard algorithm or simply process based on precedence.
    # Given the constraints and typical interview style, a two-pass or stack-based approach works.
    
    # Let's use a stack-based evaluation with precedence handling.
    # We will convert the infix expression to postfix (RPN) or evaluate directly.
    # Direct evaluation with two stacks (values and ops) is robust.
    
    values = []
    ops = []
    
    # Precedence map
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '//': 2,
        '**': 3
    }
    
    # Push the first operand
    values.append(operand[0])
    
    # Iterate through operators and operands
    for i, op in enumerate(operator):
        next_val = operand[i + 1]
        
        # While there is an operator at the top of the ops stack with greater or equal precedence
        while ops and precedence[ops[-1]] >= precedence[op]:
            # Pop operator and two values
            current_op = ops.pop()
            right_val = values.pop()
            left_val = values.pop()
            
            # Apply operation
            if current_op == '+':
                res = left_val + right_val
            elif current_op == '-':
                res = left_val - right_val
            elif current_op == '*':
                res = left_val * right_val
            elif current_op == '//':
                res = left_val // right_val
            elif current_op == '**':
                res = left_val ** right_val
            
            values.append(res)
        
        # Push current operator
        ops.append(op)
        values.append(next_val)
    
    # Process remaining operators
    while ops:
        current_op = ops.pop()
        right_val = values.pop()
        left_val = values.pop()
        
        if current_op == '+':
            res = left_val + right_val
        elif current_op == '-':
            res = left_val - right_val
        elif current_op == '*':
            res = left_val * right_val
        elif current_op == '//':
            res = left_val // right_val
        elif current_op == '**':
            res = left_val ** right_val
        
        values.append(res)
    
    return values[0]