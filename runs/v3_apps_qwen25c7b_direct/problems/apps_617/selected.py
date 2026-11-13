def max_expression_value(expression):
    import re
    from itertools import combinations
    
    # Split the expression into numbers and operators
    nums = list(map(int, re.findall(r'\d+', expression)))
    ops = list(re.findall(r'[\+\*]', expression))
    
    # Function to evaluate the expression with given bracket positions
    def evaluate(bracket_positions):
        expr = expression[:]
        for pos in sorted(bracket_positions, reverse=True):
            if pos == len(expr) - 1:
                expr = expr[:pos] + '(' + expr[pos:]
            else:
                expr = expr[:pos] + '(' + expr[pos]
        return eval(expr)
    
    # Generate all possible pairs of bracket positions
    max_value = float('-inf')
    for i in range(len(ops)):
        for j in range(i + 1, len(ops)):
            bracket_positions = [i * 2 + 1, j * 2 + 1]
            value = evaluate(bracket_positions)
            if value > max_value:
                max_value = value
    
    return max_value

# Example usage:
# result = max_expression_value("3+5*7+8*4")
# print(result)  # Output: 303