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
    operator = ['+', '*', '-']
    array = [2, 3, 4, 5]
    result = 2 + 3 * 4 - 5
    => result = 9

    Note:
        The length of operator list is equal to the length of operand list minus one.
        Operand is a list of of non-negative integers.
        Operator list has at least one operator, and operand list has at least two operands.

    """
    # Convert operands to integers to ensure type consistency
    stack = [int(x) for x in operand]
    ops = list(operator)
    
    # We will process the expression using two stacks: one for values and one for operators.
    # However, since the input is a flat sequence of (operand, op, operand, op, ...),
    # we can simulate the evaluation by respecting operator precedence.
    # Precedence: ** (highest), * and // (medium), + and - (lowest).
    
    # Let's parse the expression into tokens and then evaluate using two stacks (shunting-yard algorithm variant)
    # Or simpler: since we know the structure is alternating, we can build a list of operations and values.
    
    # Approach: Use two stacks: values and operators.
    # Iterate through the operands and operators.
    # But we need to handle precedence. So we push values and operators to stacks.
    # When we see a new operator, we compare its precedence with the top of the operator stack.
    # If the top operator has higher or equal precedence (for left-associative), we pop and evaluate.
    
    # Precedence map
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '//': 2,
        '**': 3
    }
    
    # Initial value stack with the first operand
    val_stack = [int(operand[0])]
    op_stack = []
    
    # Iterate through operators and operands
    for i, op in enumerate(ops):
        # Next operand is at operand[i+1]
        next_val = int(operand[i+1])
        
        # Check precedence: while there is an operator at the top of the stack with greater or equal precedence
        # Note: ** is right-associative, others are left-associative.
        # For right-associative (**), we only pop if the top operator has strictly greater precedence.
        while op_stack:
            top_op = op_stack[-1]
            if precedence[top_op] < precedence[op]:
                # Top operator has lower precedence, push current and break
                op_stack.append(op)
                val_stack.append(next_val)
                break
            elif precedence[top_op] > precedence[op]:
                # Top operator has higher precedence, evaluate and pop
                op_stack.pop()
                right = val_stack.pop()
                left = val_stack.pop()
                val_stack.append(eval_binary_op(left, right, top_op))
                # Continue to check next top
            elif precedence[top_op] == precedence[op]:
                # Same precedence: handle associativity
                if top_op == '**':
                    # Right associative: do not pop, push current
                    op_stack.append(op)
                    val_stack.append(next_val)
                    break
                else:
                    # Left associative: pop and evaluate
                    op_stack.pop()
                    right = val_stack.pop()
                    left = val_stack.pop()
                    val_stack.append(eval_binary_op(left, right, top_op))
                    # After popping, re-evaluate the new top if needed (loop continues)
                    # But we need to be careful not to use the 'next_val' yet.
                    # We just pushed nothing to val_stack in this iteration yet? 
                    # Actually, we haven't appended next_val to val_stack yet in this iteration.
                    # So we continue the while loop to potentially evaluate more.
        else:
            # If the while loop condition was false initially (stack empty or precedence logic handled)
            # But wait, the logic inside the while loop needs to cover the case where we push the current op.
            # Let's refactor the logic inside the loop to be cleaner.
            pass

    # Let's restart the loop logic to be more robust.
    val_stack = [int(operand[0])]
    op_stack = []
    
    for i, op in enumerate(ops):
        current_val = int(operand[i+1])
        
        # While we have operators in the stack and the current operator has lower or equal precedence (with care for **)
        while op_stack:
            top_op = op_stack[-1]
            top_prec = precedence[top_op]
            curr_prec = precedence[op]
            
            if curr_prec < top_prec:
                # Top is higher, evaluate top
                op_stack.pop()
                right = val_stack.pop()
                left = val_stack.pop()
                val_stack.append(eval_binary_op(left, right, top_op))
            elif curr_prec > top_prec:
                # Top is lower, push current and break
                op_stack.append(op)
                val_stack.append(current_val)
                break
            elif curr_prec == top_prec:
                # Same precedence
                if top_op == '**':
                    # Right associative: do not evaluate, push current
                    op_stack.append(op)
                    val_stack.append(current_val)
                    break
                else:
                    # Left associative: evaluate top
                    op_stack.pop()
                    right = val_stack.pop()
                    left = val_stack.pop()
                    val_stack.append(eval_binary_op(left, right, top_op))
                    # Continue loop to check new top
        else:
            # If while loop didn't break, it means stack became empty or we fell through
            # But the logic above ensures we either pop or push and break.
            # The only case we don't push is if we pop.
            # If we popped and the stack is still not empty, we continue.
            # If stack becomes empty, we exit loop and then push current.
            pass

        # If after the while loop, the stack is empty, we must push the current operator and value
        if not op_stack:
            op_stack.append(op)
            val_stack.append(current_val)
        # If we broke out of the loop because we pushed, we are done with this iteration.
        # If we broke out because curr_prec > top_prec, we pushed and are done.
        # If we finished the loop because stack became empty (pop until empty), we need to push current.
        # Wait, the structure above: if we pop, we continue the while loop.
        # If we pop and stack becomes empty, the while loop terminates.
        # Then we check `if not op_stack`? No, if we popped everything, stack is empty, so we push.
        # But if we pushed and broke, stack is not empty, so we don't push again.
        # Correct.

    # Final evaluation: pop all remaining operators
    while op_stack:
        op = op_stack.pop()
        right = val_stack.pop()
        left = val_stack.pop()
        val_stack.append(eval_binary_op(left, right, op))
        
    return val_stack[0]

def eval_binary_op(left, right, op):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '//':
        return left // right
    elif op == '**':
        return left ** right
    else:
        raise ValueError(f"Unknown operator: {op}")