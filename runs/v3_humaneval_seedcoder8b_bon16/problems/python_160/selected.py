def do_algebra(operator, operand):
    """
    Evaluate the algebraic expression formed by the given operator and operand lists.
    """
    expression = str(operand[0])
    
    for i in range(len(operator)):
        expression += operator[i] + str(operand[i+1])
    
    return eval(expression)