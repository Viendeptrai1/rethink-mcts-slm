import sys
from itertools import combinations

def max_expression_value(expression):
    # Split the expression into digits and operators
    digits = list(map(int, ''.join(filter(str.isdigit, expression))))
    ops = list(filter(lambda x: x in '+*', expression))
    
    # Generate all possible pairs of parentheses
    n = len(ops)
    max_result = -1
    
    for i, j in combinations(range(n + 1), 2):
        left_part = expression[:i * 2]
        middle_part = f"({expression[i * 2:i * 2 + 1]}{expression[i * 2 + 1:i * 2 + 2]}{expression[i * 2 + 2:j * 2 + 1]})"
        right_part = expression[j * 2 + 1:]
        
        # Calculate the result of the expression with the current pair of parentheses
        result = eval(left_part + middle_part + right_part)
        if result > max_result:
            max_result = result
    
    return max_result

# Read input from stdin
input_string = sys.stdin.read().strip()
# Call the function and print the result
print(max_expression_value(input_string))