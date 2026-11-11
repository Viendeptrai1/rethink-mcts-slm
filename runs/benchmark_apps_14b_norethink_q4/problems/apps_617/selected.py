def max_expression_value(s):
    def evaluate(expression):
        return eval(expression)

    max_value = float('-inf')
    n = len(s)
    
    for i in range(1, n - 1, 2):
        # Insert brackets at position i
        left_part = s[:i]
        right_part = s[i+1:]
        new_expression = f"({left_part}){s[i]}({right_part})"
        value = evaluate(new_expression)
        if value > max_value:
            max_value = value
    
    return max_value

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Print the result
print(max_expression_value(input))